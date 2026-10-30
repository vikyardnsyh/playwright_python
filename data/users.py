import os
from dataclasses import dataclass, field
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

@dataclass
class UserAccess:
    username: str
    password: str
    role: str
    role_id: int
    welcome_title: str
    dashboard_url: str
    accessible_menus: List[str] = field(default_factory=list)


# 1. Administrator User Access
ADMIN_USER = UserAccess(
    username=os.getenv("ADMIN_USER", "ayu"),
    password=os.getenv("ADMIN_PASS", "rahasia"),
    role="Admin",
    role_id=2,
    welcome_title="HALLO ADMIN",
    dashboard_url="/",
    accessible_menus=[
        "Dashboard",
        "Administrasi Data Akun",
        "Administrasi Data Dokter",
        "Administrasi Pendaftaran",
        "Administrasi Anggota",
        "Download Laporan",
    ]
)

# 2. Doctor / Member User Access
MEMBER_USER = UserAccess(
    username=os.getenv("REG_USER", "aldy"),
    password=os.getenv("REG_PASS", "PdhiBanten2!"),
    role="Dokter",
    role_id=1,
    welcome_title="HALLO DOKTER",
    dashboard_url="/",
    accessible_menus=[
        "Home",
        "Form Registrasi Anggota",
        "Upload Berkas",
        "Syarat Pendaftaran Anggota",
        "Ubah Password",
    ]
)

# User registry mapping
USERS_MAP: Dict[str, UserAccess] = {
    "admin": ADMIN_USER,
    "dokter": MEMBER_USER,
    "member": MEMBER_USER,
}

def get_user(role_or_key: str) -> UserAccess:
    """Retrieve user credentials and metadata by role name or key."""
    key = role_or_key.lower().strip()
    if key in USERS_MAP:
        return USERS_MAP[key]
    raise ValueError(f"Unknown user role '{role_or_key}'. Available: {list(USERS_MAP.keys())}")
