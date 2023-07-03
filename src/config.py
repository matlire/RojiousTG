from dataclasses import dataclass

@dataclass
class Config:
    show_name:    str = ""
    username:     str = ""
    token:        str = ""
    description:  str = ""
    about:        str = ""
    client_id:    str = ""
    redirect_uri: str = ""
    access_token: str = ""
    db_file:      str = "db.db"
