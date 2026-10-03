*&---------------------------------------------------------------------*
*& Report ZBC_COND_TABLE_PRECHECK
*&---------------------------------------------------------------------*
*& Checks generated condition tables (Axxx) for the problems that stop
*& dictionary activation when the post-import method
*& RV_COND_TABLE_GEN_ACT_METHOD runs in the target system.
*&
*& Run it in the development system before releasing a request
*& (catches the problem at source), and in QAS/PRD after an import
*& ends with RC 8 (tells Basis which tables fail and why).
*&
*& Checks per table:
*&   KEY16   more than 16 key fields (DDIC hard limit)
*&   STATE   table exists only as an inactive version
*&   KOMG    field is not in the condition field structure KOMG
*&   DTEL    field's data element is not active in this system
*&---------------------------------------------------------------------*
REPORT zbc_cond_table_precheck.

TABLES dd02l.

SELECT-OPTIONS s_tab FOR dd02l-tabname DEFAULT 'A9*' OPTION CP.
PARAMETERS p_state TYPE ddobjstate DEFAULT 'M'. " M = newest version (active or inactive)

CONSTANTS gc_max_keys TYPE i VALUE 16.

TYPES: BEGIN OF ty_result,
         severity TYPE char5,
         tabname  TYPE tabname,
         ddstate  TYPE ddobjstate,
         keys     TYPE i,
         var_keys TYPE i,
         rule     TYPE char8,
         detail   TYPE char255,
       END OF ty_result,
       ty_results TYPE STANDARD TABLE OF ty_result WITH EMPTY KEY.

CLASS lcl_check DEFINITION FINAL.
  PUBLIC SECTION.
    METHODS constructor.
    METHODS run
      IMPORTING it_tabnames      TYPE string_table
      RETURNING VALUE(rt_result) TYPE ty_results.
  PRIVATE SECTION.
    DATA mt_komg TYPE HASHED TABLE OF fieldname WITH UNIQUE KEY table_line.
    METHODS check_table
      IMPORTING iv_tabname       TYPE tabname
      RETURNING VALUE(rt_result) TYPE ty_results.
    CLASS-METHODS is_fixed_field
      IMPORTING iv_field       TYPE fieldname
      RETURNING VALUE(rv_yes)  TYPE abap_bool.
ENDCLASS.

CLASS lcl_check IMPLEMENTATION.

  METHOD constructor.
    " All fields a condition table may use come from KOMG (incl. appends).
    DATA lt_dfies TYPE STANDARD TABLE OF dfies.
    CALL FUNCTION 'DDIF_FIELDINFO_GET'
      EXPORTING
        tabname   = 'KOMG'
      TABLES
        dfies_tab = lt_dfies
      EXCEPTIONS
        OTHERS    = 1.
    IF sy-subrc = 0.
      mt_komg = VALUE #( FOR ls IN lt_dfies ( ls-fieldname ) ).
    ENDIF.
  ENDMETHOD.

  METHOD is_fixed_field.
    rv_yes = xsdbool( iv_field = 'MANDT' OR iv_field = 'KAPPL' OR iv_field = 'KSCHL'
                   OR iv_field = 'KFRST' OR iv_field = 'DATBI' OR iv_field = 'DATAB'
                   OR iv_field = 'KBSTAT' OR iv_field = 'KNUMH' ).
  ENDMETHOD.

  METHOD run.
    LOOP AT it_tabnames INTO DATA(lv_tab).
      APPEND LINES OF check_table( CONV #( lv_tab ) ) TO rt_result.
    ENDLOOP.
  ENDMETHOD.

  METHOD check_table.
    DATA: lv_got   TYPE ddgotstate,
          ls_dd02v TYPE dd02v,
          lt_dd03p TYPE STANDARD TABLE OF dd03p,
          ls_res   TYPE ty_result.

    CALL FUNCTION 'DDIF_TABL_GET'
      EXPORTING
        name          = iv_tabname
        state         = p_state
        langu         = sy-langu
      IMPORTING
        gotstate      = lv_got
        dd02v_wa      = ls_dd02v
      TABLES
        dd03p_tab     = lt_dd03p
      EXCEPTIONS
        illegal_input = 1
        OTHERS        = 2.
    IF sy-subrc <> 0 OR lv_got IS INITIAL.
      APPEND VALUE #( severity = 'ERROR' tabname = iv_tabname rule = 'MISSING'
                      detail = 'No dictionary definition found in this system' ) TO rt_result.
      RETURN.
    ENDIF.

    DELETE lt_dd03p WHERE fieldname(1) = '.'.   " .INCLUDE / .APPEND rows

    DATA(lv_keys) = REDUCE i( INIT n = 0 FOR f IN lt_dd03p WHERE ( keyflag = abap_true ) NEXT n = n + 1 ).
    DATA(lv_var)  = REDUCE i( INIT n = 0 FOR f IN lt_dd03p
                              WHERE ( keyflag = abap_true ) NEXT n = n + COND i( WHEN is_fixed_field( f-fieldname ) = abap_true THEN 0 ELSE 1 ) ).

    DATA(ls_base) = VALUE ty_result( tabname = iv_tabname ddstate = lv_got keys = lv_keys var_keys = lv_var ).
    DATA(lv_found) = abap_false.

    " KEY16: dictionary hard limit
    IF lv_keys > gc_max_keys.
      ls_res = ls_base.
      ls_res-severity = 'ERROR'.
      ls_res-rule     = 'KEY16'.
      ls_res-detail   = |{ lv_keys } key fields (limit { gc_max_keys }); reduce variable keys from { lv_var } to { lv_var - ( lv_keys - gc_max_keys ) } or fewer|.
      APPEND ls_res TO rt_result.
      lv_found = abap_true.
    ENDIF.

    " KOMG / DTEL: every field must exist in KOMG and have an active data element
    LOOP AT lt_dd03p INTO DATA(ls_field).
      IF is_fixed_field( ls_field-fieldname ) = abap_false
         AND mt_komg IS NOT INITIAL
         AND NOT line_exists( mt_komg[ table_line = ls_field-fieldname ] ).
        ls_res = ls_base.
        ls_res-severity = 'ERROR'.
        ls_res-rule     = 'KOMG'.
        ls_res-detail   = |Field { ls_field-fieldname } is not in KOMG: import the append / custom field request first|.
        APPEND ls_res TO rt_result.
        lv_found = abap_true.
      ENDIF.

      IF ls_field-rollname IS NOT INITIAL.
        SELECT SINGLE @abap_true FROM dd04l
          WHERE rollname = @ls_field-rollname AND as4local = 'A'
          INTO @DATA(lv_dtel_ok).
        IF sy-subrc <> 0.
          ls_res = ls_base.
          ls_res-severity = 'ERROR'.
          ls_res-rule     = 'DTEL'.
          ls_res-detail   = |Data element { ls_field-rollname } (field { ls_field-fieldname }) is not active|.
          APPEND ls_res TO rt_result.
          lv_found = abap_true.
        ENDIF.
        CLEAR lv_dtel_ok.
      ENDIF.
    ENDLOOP.

    " STATE: only an inactive version exists and no cause was found above
    IF lv_got <> 'A' AND lv_found = abap_false.
      ls_res = ls_base.
      ls_res-severity = 'WARN'.
      ls_res-rule     = 'STATE'.
      ls_res-detail   = 'Inactive, no known cause found: open SE11 > Utilities > Activation Log'.
      APPEND ls_res TO rt_result.
      lv_found = abap_true.
    ENDIF.

    IF lv_found = abap_false.
      ls_res = ls_base.
      ls_res-severity = 'OK'.
      ls_res-detail   = |{ lv_keys } key fields, all fields resolvable|.
      APPEND ls_res TO rt_result.
    ENDIF.
  ENDMETHOD.

ENDCLASS.

START-OF-SELECTION.
  SELECT DISTINCT tabname FROM dd02l
    WHERE tabname IN @s_tab
      AND tabclass = 'TRANSP'
      AND as4local IN ( 'A', 'N' )
    ORDER BY tabname
    INTO TABLE @DATA(lt_tabs).

  DATA(lt_names) = VALUE string_table( FOR t IN lt_tabs ( CONV string( t-tabname ) ) ).
  DATA(lt_result) = NEW lcl_check( )->run( lt_names ).

  SORT lt_result BY severity tabname.   " alphabetical: ERROR rows come first

  TRY.
      cl_salv_table=>factory( IMPORTING r_salv_table = DATA(lo_alv)
                              CHANGING  t_table      = lt_result ).
      lo_alv->get_columns( )->set_optimize( abap_true ).
      lo_alv->get_functions( )->set_all( abap_true ).
      lo_alv->get_display_settings( )->set_list_header(
        |Condition table pre-check: { lines( lt_tabs ) } tables, { REDUCE i( INIT n = 0 FOR r IN lt_result WHERE ( severity = 'ERROR' ) NEXT n = n + 1 ) } errors| ).
      lo_alv->display( ).
    CATCH cx_salv_msg INTO DATA(lx).
      MESSAGE lx TYPE 'E'.
  ENDTRY.
