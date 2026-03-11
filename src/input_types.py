"""Typed dataclasses for Native_in_* and Scaffold_in_* input files.

Use dataclasses.asdict() for logging, JSON export, or ML feature tables:
    from dataclasses import asdict
    native_dict = asdict(native)
    scaffold_dict = asdict(scaffold)
"""

from dataclasses import dataclass


@dataclass
class ScaffoldParams:
    vessel_name: str
    radius: float
    thickness: float

    c1_p1: float
    c2_p1: float
    c1_p2: float
    c2_p2: float

    eta_p1_h: float
    eta_p2_h: float

    g_p1_h: float
    g_p2_h: float

    rho_hat_p1: float
    rho_hat_p2: float

    epsilon_p1_0: float
    epsilon_p2_0: float

    k_p1: float
    zeta_p1: float
    k_p2: float
    zeta_p2: float

    fd_p1: float
    fd_p2: float


@dataclass
class NativeParams:
    vessel_name: str
    radius: float
    thickness: float

    lambda_z_h: float

    c1_e: float
    c2_e: float
    c1_m: float
    c2_m: float
    c1_ct: float
    c2_ct: float
    c1_cz: float
    c2_cz: float
    c1_cd1: float
    c2_cd1: float
    c1_cd2: float
    c2_cd2: float

    eta_e_h: float
    eta_m_h: float
    eta_ct_h: float
    eta_cz_h: float
    eta_cd1_h: float
    eta_cd2_h: float

    G_e_rh: float
    G_e_thh: float
    G_e_zh: float

    G_h_e: float
    G_h_m: float
    G_h_ct: float
    G_h_cz: float
    G_h_cd1: float
    G_h_cd2: float

    rho_hat_h: float

    phi_e_h: float
    phi_m_h: float
    phi_ct_h: float
    phi_cz_h: float
    phi_cd1_h: float
    phi_cd2_h: float

    k_e_h: float
    k_m_h: float
    k_ct_h: float
    k_cz_h: float
    k_cd1_h: float
    k_cd2_h: float

    K_sigma_p_e: float
    K_sigma_p_m: float
    K_sigma_p_ct: float
    K_sigma_p_cz: float
    K_sigma_p_cd1: float
    K_sigma_p_cd2: float

    K_sigma_d_e: float
    K_sigma_d_m: float
    K_sigma_d_ct: float
    K_sigma_d_cz: float
    K_sigma_d_cd1: float
    K_sigma_d_cd2: float

    K_tauw_p_e: float
    K_tauw_p_m: float
    K_tauw_p_ct: float
    K_tauw_p_cz: float
    K_tauw_p_cd1: float
    K_tauw_p_cd2: float

    K_tauw_d_e: float
    K_tauw_d_m: float
    K_tauw_d_ct: float
    K_tauw_d_cz: float
    K_tauw_d_cd1: float
    K_tauw_d_cd2: float

    P_h: float
    Q_h: float

    k_act: float
    lambda_0: float
    lambda_m: float

    C_B: float
    C_S: float

    T_act_h: float
