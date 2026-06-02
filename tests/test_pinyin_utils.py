"""Tests for pinyin_utils.py."""

from academic_ime.pinyin_utils import term_to_pinyin


def test_cjk_only() -> None:
    """Pure Chinese text → pinyin."""
    assert term_to_pinyin("范数溢出") == "fan shu yi chu"
    assert term_to_pinyin("综合数据") == "zong he shu ju"


def test_english_only() -> None:
    """Pure English text → lowercased."""
    assert term_to_pinyin("ffSampling") == "ffsampling"
    assert term_to_pinyin("SamplerZ") == "samplerz"
    assert term_to_pinyin("FPU") == "fpu"
    assert term_to_pinyin("trade-off") == "trade-off"


def test_mixed_falcon_signature() -> None:
    """Falcon签名流程 → falcon qian ming liu cheng."""
    assert term_to_pinyin("Falcon签名流程") == "falcon qian ming liu cheng"


def test_mixed_ntt_module() -> None:
    """NTT模块 → ntt mo kuai."""
    assert term_to_pinyin("NTT模块") == "ntt mo kuai"


def test_mixed_smic40nm() -> None:
    """SMIC40nm工艺 → smic40nm gong yi."""
    assert term_to_pinyin("SMIC40nm工艺") == "smic40nm gong yi"


def test_mixed_ffsampling_module() -> None:
    """ffSampling模块 → ffsampling mo kuai."""
    assert term_to_pinyin("ffSampling模块") == "ffsampling mo kuai"


def test_mixed_ml_kem() -> None:
    """ML-KEM算法 → ml-kem suan fa."""
    assert term_to_pinyin("ML-KEM算法") == "ml-kem suan fa"


def test_mixed_fpu_fft() -> None:
    """FPU/FFT精度 → fpu/fft jing du."""
    assert term_to_pinyin("FPU/FFT精度") == "fpu/fft jing du"


def test_mixed_tradeoff() -> None:
    """性能面积trade-off → xing neng mian ji trade-off."""
    result = term_to_pinyin("性能面积trade-off")
    assert result == "xing neng mian ji trade-off"


def test_empty_string() -> None:
    """Empty string returns empty."""
    assert term_to_pinyin("") == ""
