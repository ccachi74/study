* 개발서버에서는 정상 실행됨.
* 운영서버에서는 404 에러 발생
* 방화벽 해제 요청 후 오류 해결
* URL을 HTTPS 로 변경 시 500 에러 발생
* T-CODE 'STRUST' 에서 접속대상 사이트 인증서 등록 필요

REPORT ZCMS_API_01.

DATA: LO_CLIENT  TYPE REF TO IF_HTTP_CLIENT,
      LD_DATA    TYPE STRING,
      LD_STREAM  TYPE STRING.

DATA: STRINGTAB  TYPE STANDARD TABLE OF STRING,
      WA_STRING  TYPE STRING.

PARAMETERS P_URL TYPE STRING DEFAULT 'http://dlapi-dev.mobis.co.kr/dl/sl100/v1' LOWER CASE.

" HTTP Client 생성
CL_HTTP_CLIENT=>CREATE_BY_URL(
    EXPORTING
        URL = P_URL
    IMPORTING
        CLIENT = LO_CLIENT
    EXCEPTIONS
        ARGUMENT_NOT_FOUND = 1
        PLUGIN_NOT_ACTIVE  = 2
        INTERNAL_ERROR     = 3
        OTHERS             = 4 ).

* JSON 형식 테스트 데이터 준비
LD_DATA = LD_DATA && '{'.
LD_DATA = LD_DATA && '    "IF_INFO": {'.
LD_DATA = LD_DATA && '        "if_id": "DLSL001",'.
LD_DATA = LD_DATA && '        "if_key": "66b173ec-8e7a-46d4-834b-f5bf8fce24e4",'.
LD_DATA = LD_DATA && '        "if_data_cnt": 1'.
LD_DATA = LD_DATA && '    },'.
LD_DATA = LD_DATA && '    "IF_DATA": ['.
LD_DATA = LD_DATA && '        {'.
LD_DATA = LD_DATA && '            "log_clct_dt": "20200908192355",'.
LD_DATA = LD_DATA && '            "log_div_cd": "CN",'.
LD_DATA = LD_DATA && '            "seq_no": 1,'.
LD_DATA = LD_DATA && '            "sys_div_cd": "SMART",'.
LD_DATA = LD_DATA && '            "user_ip_addr": "211.39.123.456",'.
LD_DATA = LD_DATA && '            "user_id": "066423",'.
LD_DATA = LD_DATA && '            "empno": "DT066423",'.
LD_DATA = LD_DATA && '            "user_nm": "홍길동",'.
LD_DATA = LD_DATA && '            "user_team_nm": "정보보호팀",'.
LD_DATA = LD_DATA && '            "admin_grad_acnt_yn": "Y",'.
LD_DATA = LD_DATA && '            "url_val": "SearchLoginHistory.do",'.
LD_DATA = LD_DATA && '            "http_rqst_val": null,'.
LD_DATA = LD_DATA && '            "log_clct_utc": "20200908192355",'.
LD_DATA = LD_DATA && '            "login_sucs_yn": "N"'.
LD_DATA = LD_DATA && '        }'.
LD_DATA = LD_DATA && '    ]'.
LD_DATA = LD_DATA && '}'.

* Prepare Request
LO_CLIENT->REQUEST->SET_METHOD( IF_HTTP_REQUEST=>CO_REQUEST_METHOD_POST ).
LO_CLIENT->REQUEST->SET_HEADER_FIELD( NAME = 'Content-Type' VALUE = 'application/json; charset="utf-8"' ).
LO_CLIENT->REQUEST->SET_CDATA( DATA = LD_DATA ).

* Request 전송
LO_CLIENT->SEND(
    EXCEPTIONS
        HTTP_COMMUNICATION_FAILURE = 1
        HTTP_INVALID_STATE         = 2
        HTTP_PROCESSING_FAILED     = 3
        OTHERS                     = 4 ).

* 전송결과 수신
LO_CLIENT->RECEIVE(
    EXCEPTIONS
    HTTP_COMMUNICATION_FAILURE = 1
    HTTP_INVALID_STATE         = 2
    HTTP_PROCESSING_FAILED     = 3
    OTHERS                     = 4 ).

* Response 데이터 수신
LD_STREAM = LO_CLIENT->RESPONSE->GET_CDATA( ).

* 결과 출력
WRITE:/ LD_DATA.
WRITE:/ 'Response'.

SPLIT LD_STREAM AT ',' INTO TABLE STRINGTAB.
LOOP AT STRINGTAB INTO WA_STRING
    WRITE:/ WA_STRING.
ENDLOOP.

LO_CLIENT->CLOSE().
