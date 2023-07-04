from dataclasses import dataclass

@dataclass
class Config:
    show_name:    str = ""
    username:     str = ""
    token:        str = ""
    description:  str = ""
    about:        str = ""
    client_id:    str = "" # From yoomoney
    redirect_uri: str = "" # From yoomoney
    access_token: str = "" # From yoomoney
    db_file:      str = "db.db"
