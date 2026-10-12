import pytest

from validation_catalog import describe_validation


@pytest.mark.parametrize(
    "name",
    [
        "N=16 sector dimensions sum",
        "N=2 singlet energy",
        "spin translation entries are +1",
        "Hermiticity J2=0",
        "[H,T]=0 J2=0.5",
        "P_k orthonormality J2=0",
        "T P_k=e^(ik) P_k J2=0.5",
        "sum momentum dimensions J2=0",
        "U(1) vs block ground J2=0.5",
        "normalized structure-factor sum rule J2=0",
        "N=8 block-spectrum union J2=0.5",
        "MG ED ground energy N=12",
        "XX free-fermion N=10",
        "FAULT: wrong Jordan-Wigner boundary is detected for N=8",
    ],
)
def test_validation_description_names_error_and_failure_signature(name):
    description = describe_validation(name)
    assert len(description.targeted_error) >= 12
    assert len(description.failure_signature) >= 12
    assert "未分类" not in description.targeted_error
    assert "未分类" not in description.failure_signature


def test_unknown_validation_name_is_rejected():
    with pytest.raises(KeyError):
        describe_validation("unknown check")
