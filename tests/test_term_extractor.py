"""Tests for term_extractor.py."""

from academic_ime.term_extractor import extract_terms

SAMPLE_TEXT = """
本周完成 Falcon 签名流程联调，重点针对当前范数溢出问题进行定位分析，
排查采样参数读取、SamplerZ 输出、FPU/FFT 精度以及范数计算逻辑等环节。
同时完善 Falcon Tree 与 ffSampling 之间的参数读取、缓存管理和数据调度接口，
继续开展 ffSampling、SamplerZ、FPU/FFT 的联合仿真，并整理阶段性调试结果和性能情况。
单 FPU 方案约需要 51w cycles，双 FPU 方案约需要 45w cycles。
后续计划进行综合，分析资源占用、综合数据以及性能面积 trade-off。
"""


def test_extract_falcon_signature() -> None:
    """Should extract 'Falcon签名'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "Falcon签名" in terms


def test_extract_fan_shu_yi_chu() -> None:
    """Should extract '范数溢出'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "范数溢出" in terms


def test_extract_samplerz_output() -> None:
    """Should extract 'SamplerZ输出'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "SamplerZ输出" in terms


def test_extract_ffsampling() -> None:
    """Should extract 'ffSampling'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "ffSampling" in terms


def test_extract_fpu_fft() -> None:
    """Should extract 'FPU/FFT'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "FPU/FFT" in terms


def test_extract_zong_he_shu_ju() -> None:
    """Should extract '综合数据'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "综合数据" in terms


def test_extract_trade_off() -> None:
    """Should extract 'trade-off'."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "trade-off" in terms


def test_extract_ntt() -> None:
    """Should extract 'FPU' (acronym)."""
    terms = extract_terms(SAMPLE_TEXT)
    assert "FPU" in terms
