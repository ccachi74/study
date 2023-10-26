str = '''{
    "IF_INFO" : {
        "if_id" : "DLSL001",
        "if_key" : "66b173ec-8e7a-46d4-834b-f5bf8fce24e4",
        "if_data_cnt" : 3
    },
    "IF_DATA" : [
{
    "log_clct_dt" : "20200908192355",
    "log_div_cd" : "CN",
    "seq_no" : 1,
    "sys_div_cd" : "SMART",
    "user_ip_addr" : "211.39.123.456",
    "user_id" : "066423",
    "empno" : "DT066423",
    "user_nm" : "홍길동",
    "user_team_nm" : "정보보호팀",
    "admin_grad_acnt_yn" : "Y",
    "url_val" : "SearchLoginHistory.do",
    "http_rqst_val" : { 
        "search_s_date" : "20200101",
        "title" : "공지"
    },
    "log_clct_utc" : "20200908192355",
    "login_sucs_yn" : "N"
}'''


new_str = str.replace('\n', '')
new_str = new_str.replace(' ', '')

print(new_str)