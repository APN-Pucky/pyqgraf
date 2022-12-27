"""" 
Collection of qgraf models

From:

* https://porthos.tecnico.ulisboa.pt/CTQFT/node9.html
* ...

"""
import re


def multiple_replace(string, rep_dict):
    pattern = re.compile(
        "|".join([re.escape(k) for k in sorted(rep_dict, key=len, reverse=True)]),
        flags=re.DOTALL,
    )
    return pattern.sub(lambda x: rep_dict[x.group(0)], string)


def rename(raw_model):
    """
    Rename particles in a qgraf model.

    We use programatic names from particles python package.

    """
    return multiple_replace(
        raw_model,
        {
            # leptons
            "e": "e_minus",
            "e1": "e_minus",
            "e2": "mu_minus",
            "e3": "tau_minus",
            "E": "e_plus",
            "E1": "e_plus",
            "E2": "mu_plus",
            "E3": "tau_plus",
            # neutrinos
            "n": "nu_e",
            "n1": "nu_e",
            "n2": "nu_mu",
            "n3": "nu_tau",
            "N": "nu_e_bar",
            "N1": "nu_e_bar",
            "N2": "nu_mu_bar",
            "N3": "nu_tau_bar",
            # quarks
            "u": "u",
            "c": "c",
            "t": "t",
            "d": "d",
            "s": "s",
            "b": "b",
            "U": "u_bar",
            "C": "c_bar",
            "T": "t_bar",
            "D": "d_bar",
            "S": "s_bar",
            "B": "b_bar",
            # gauge bosons
            "g": "g",
            "H": "H_0",
            "Z": "Z_0",
            "WP": "W_plus",
            "WM": "W_minus",
            "A": "gamma",
        },
    )


qed = rename(
    r"""
*   leptons

  [e,E,-]

*      photon

  [A,A,+]

* fermion - gauge boson

  [E,e,A]
"""
)
gws_UnitaryGauge = rename(
    r"""

*                  Higgs

  [H,H,+]

*   electron, muon, tau

  [e1,E1,-]
  [e2,E2,-]
  [e3,E3,-]

*                  neutrinos

  [n1,N1,-]
  [n2,N2,-]
  [n3,N3,-]

*              quarks

  [u,U,-]
  [c,C,-]
  [t,T,-]
  [d,D,-]
  [s,S,-]
  [b,B,-]


*      photon, W-boson, Z-boson, gluon

  [A,A,+]
  [WM,WP,+]
  [Z,Z,+]
  [g,g,+]

*                 cubic vertices


  [WP,WM,A]
  [WP,WM,Z]
  [g,g,g]


  [WP,WM,H]
  [Z,Z,H]
  [H,H,H]

* yukawa

*  [E1,e1,H]
*  [E2,e2,H]
*  [E3,e3,H]

  [U,u,H]
  [C,c,H]
  [T,t,H]
  [D,d,H]
  [S,s,H]
  [B,b,H]

* fermion - gauge boson

  [E1,e1,A]
  [E2,e2,A]
  [E3,e3,A]

  [E1,e1,Z]
  [E2,e2,Z]
  [E3,e3,Z]

  [N1,n1,Z]
  [N2,n2,Z]
  [N3,n3,Z]

  [N1,e1,WP]
  [N2,e2,WP]
  [N3,e3,WP]

  [E1,n1,WM]
  [E2,n2,WM]
  [E3,n3,WM]

  [U,u,A]
  [C,c,A]
  [T,t,A]
  [D,d,A]
  [S,s,A]
  [B,b,A]

  [U,u,Z]
  [C,c,Z]
  [T,t,Z]
  [D,d,Z]
  [S,s,Z]
  [B,b,Z]


  [U,u,g]
  [C,c,g]
  [T,t,g]
  [D,d,g]
  [S,s,g]
  [B,b,g]

* K-M

  [U,d,WP]
  [U,s,WP]
  [U,b,WP]

  [C,d,WP]
  [C,s,WP]
  [C,b,WP]

  [T,d,WP]
  [T,s,WP]
  [T,b,WP]

  [D,u,WM]
  [D,c,WM]
  [D,t,WM]

  [S,u,WM]
  [S,c,WM]
  [S,t,WM]

  [B,u,WM]
  [B,c,WM]
  [B,t,WM]


*                     quartic vertices

  [WP,WM,A,A]
  [WP,WM,Z,Z]
  [WP,WM,A,Z]
  [WP,WM,WP,WM]
  [g,g,g,g]

  [WP,WM,H,H]
  [Z,Z,H,H]
  [H,H,H,H]
"""
)


gws_UnitaryGauge_reduced = rename(
    r"""

*                  Higgs

*  [H,H,+]

*   leptons

  [e,E,-]

*                  neutrinos

  [n,N,-]

*              quarks

* [u,U,-]
* [d,D,-]


*      photon, W-boson, Z-boson, gluon

  [A,A,+]
  [WM,WP,+]
  [Z,Z,+]
* [g,g,+]

*                 cubic vertices


  [WP,WM,A]
  [WP,WM,Z]
* [g,g,g]


*  [WP,WM,H]
*  [Z,Z,H]
*  [H,H,H]

* yukawa

*  [E1,e1,H]
*  [E2,e2,H]
*  [E3,e3,H]

* [U,u,H]
* [D,d,H]

* fermion - gauge boson

  [E,e,A]

  [E,e,Z]

  [N,n,Z]

  [N,e,WP]

  [E,n,WM]

* [U,u,A]
* [D,d,A]

* [U,u,Z]
* [D,d,Z]


* [U,u,g]
* [D,d,g]

* K-M

* [U,d,WP]

* [D,u,WM]


*                     quartic vertices

  [WP,WM,A,A]
*  [WP,WM,Z,Z]
*  [WP,WM,A,Z]
*  [WP,WM,WP,WM]
* [g,g,g,g]

*  [WP,WM,H,H]
*  [Z,Z,H,H]
*  [H,H,H,H]

"""
)
