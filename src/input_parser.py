"""Parse Native_in_* and Scaffold_in_* input files.

Comment lines starting with '#' are ignored. Tokens are read in fixed order
and mapped into typed dataclasses.

Example:
    from src.input_parser import parse_native_file, parse_scaffold_file

    scaffold = parse_scaffold_file("Scaffold_in_Lamb.txt")
    native = parse_native_file("Native_in_Lamb.txt")

    print(scaffold)
    print(native.P_h, native.Q_h)
"""

from pathlib import Path
from typing import List, Union

from input_types import ImmuneParams, NativeParams, ScaffoldParams


def _clean_tokens(filepath: Union[str, Path]) -> List[str]:
    """
    Read file and return non-comment, non-empty tokens.
    Comment lines beginning with '#' are skipped.
    """
    tokens: List[str] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                continue
            tokens.extend(stripped.split())
    return tokens


class TokenReader:
    def __init__(self, tokens: List[str]) -> None:
        self.tokens = tokens
        self.i = 0

    def read_str(self) -> str:
        if self.i >= len(self.tokens):
            raise ValueError("Unexpected end of file while reading string.")
        value = self.tokens[self.i]
        self.i += 1
        return value

    def read_float(self) -> float:
        if self.i >= len(self.tokens):
            raise ValueError("Unexpected end of file while reading float.")
        try:
            value = float(self.tokens[self.i])
        except ValueError as e:
            raise ValueError(
                f"Expected float at token index {self.i}, got {self.tokens[self.i]!r}"
            ) from e
        self.i += 1
        return value

    def done(self) -> bool:
        return self.i == len(self.tokens)


def parse_scaffold_file(filepath: Union[str, Path]) -> ScaffoldParams:
    t = TokenReader(_clean_tokens(filepath))

    params = ScaffoldParams(
        vessel_name=t.read_str(),
        radius=t.read_float(),
        thickness=t.read_float(),
        c1_p1=t.read_float(),
        c2_p1=t.read_float(),
        c1_p2=t.read_float(),
        c2_p2=t.read_float(),
        eta_p1_h=t.read_float(),
        eta_p2_h=t.read_float(),
        g_p1_h=t.read_float(),
        g_p2_h=t.read_float(),
        rho_hat_p1=t.read_float(),
        rho_hat_p2=t.read_float(),
        epsilon_p1_0=t.read_float(),
        epsilon_p2_0=t.read_float(),
        k_p1=t.read_float(),
        zeta_p1=t.read_float(),
        k_p2=t.read_float(),
        zeta_p2=t.read_float(),
        fd_p1=t.read_float(),
        fd_p2=t.read_float(),
    )

    if not t.done():
        raise ValueError(
            f"Scaffold file has extra unread tokens starting at index {t.i}: "
            f"{t.tokens[t.i:t.i+10]}"
        )

    return params


def parse_native_file(filepath: Union[str, Path]) -> NativeParams:
    t = TokenReader(_clean_tokens(filepath))

    params = NativeParams(
        vessel_name=t.read_str(),
        radius=t.read_float(),
        thickness=t.read_float(),
        lambda_z_h=t.read_float(),
        c1_e=t.read_float(),
        c2_e=t.read_float(),
        c1_m=t.read_float(),
        c2_m=t.read_float(),
        c1_ct=t.read_float(),
        c2_ct=t.read_float(),
        c1_cz=t.read_float(),
        c2_cz=t.read_float(),
        c1_cd1=t.read_float(),
        c2_cd1=t.read_float(),
        c1_cd2=t.read_float(),
        c2_cd2=t.read_float(),
        eta_e_h=t.read_float(),
        eta_m_h=t.read_float(),
        eta_ct_h=t.read_float(),
        eta_cz_h=t.read_float(),
        eta_cd1_h=t.read_float(),
        eta_cd2_h=t.read_float(),
        G_e_rh=t.read_float(),
        G_e_thh=t.read_float(),
        G_e_zh=t.read_float(),
        G_h_e=t.read_float(),
        G_h_m=t.read_float(),
        G_h_ct=t.read_float(),
        G_h_cz=t.read_float(),
        G_h_cd1=t.read_float(),
        G_h_cd2=t.read_float(),
        rho_hat_h=t.read_float(),
        phi_e_h=t.read_float(),
        phi_m_h=t.read_float(),
        phi_ct_h=t.read_float(),
        phi_cz_h=t.read_float(),
        phi_cd1_h=t.read_float(),
        phi_cd2_h=t.read_float(),
        k_e_h=t.read_float(),
        k_m_h=t.read_float(),
        k_ct_h=t.read_float(),
        k_cz_h=t.read_float(),
        k_cd1_h=t.read_float(),
        k_cd2_h=t.read_float(),
        K_sigma_p_e=t.read_float(),
        K_sigma_p_m=t.read_float(),
        K_sigma_p_ct=t.read_float(),
        K_sigma_p_cz=t.read_float(),
        K_sigma_p_cd1=t.read_float(),
        K_sigma_p_cd2=t.read_float(),
        K_sigma_d_e=t.read_float(),
        K_sigma_d_m=t.read_float(),
        K_sigma_d_ct=t.read_float(),
        K_sigma_d_cz=t.read_float(),
        K_sigma_d_cd1=t.read_float(),
        K_sigma_d_cd2=t.read_float(),
        K_tauw_p_e=t.read_float(),
        K_tauw_p_m=t.read_float(),
        K_tauw_p_ct=t.read_float(),
        K_tauw_p_cz=t.read_float(),
        K_tauw_p_cd1=t.read_float(),
        K_tauw_p_cd2=t.read_float(),
        K_tauw_d_e=t.read_float(),
        K_tauw_d_m=t.read_float(),
        K_tauw_d_ct=t.read_float(),
        K_tauw_d_cz=t.read_float(),
        K_tauw_d_cd1=t.read_float(),
        K_tauw_d_cd2=t.read_float(),
        P_h=t.read_float(),
        Q_h=t.read_float(),
        k_act=t.read_float(),
        lambda_0=t.read_float(),
        lambda_m=t.read_float(),
        C_B=t.read_float(),
        C_S=t.read_float(),
        T_act_h=t.read_float(),
    )

    if not t.done():
        raise ValueError(
            f"Native file has extra unread tokens starting at index {t.i}: "
            f"{t.tokens[t.i:t.i+10]}"
        )

    return params


def parse_immune_file(filepath: Union[str, Path]) -> ImmuneParams:
    t = TokenReader(_clean_tokens(filepath))

    params = ImmuneParams(
        gamma_i_1=t.read_float(),
        gamma_i_2=t.read_float(),
        gamma_p_d1=t.read_float(),
        K_i_p_mic=t.read_float(),
        K_i_p_wound=t.read_float(),
        K_i_d_max=t.read_float(),
        delta_i_p=t.read_float(),
        beta_i_p=t.read_float(),
        ps_norm=t.read_float(),
        fd_norm=t.read_float(),
        infl_scale_trans=t.read_float(),
        window_end=t.read_float(),
        rat_smc2col_p=t.read_float(),
        rat_smc2col_d=t.read_float(),
    )

    if not t.done():
        raise ValueError(
            f"Immune file has extra unread tokens starting at index {t.i}: "
            f"{t.tokens[t.i:t.i+10]}"
        )

    return params
