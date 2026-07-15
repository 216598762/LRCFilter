"""Instrumental detection module for identifying tracks with no vocals."""

from lrcfilter.config import MIN_WORDS_FOR_VOCALS, MIN_SPEECH_DURATION
from lrcfilter.models import TranscriptionResult, InstrumentalResult


def detect_instrumental(transcription: TranscriptionResult) -> InstrumentalResult:
    """
    Detect if a track is instrumental (no vocals).
    
    Args:
        transcription: Transcription result from Whisper
        
    Returns:
        InstrumentalResult with detection results
    """
    # Count words in transcription
    word_count = len(transcription.text.split()) if transcription.text else 0
    
    # Calculate total speech duration from segments
    speech_duration = 0.0
    for segment in transcription.segments:
        speech_duration += segment.end - segment.start
    
    # Determine if instrumental
    is_instrumental = (
        not transcription.has_speech or
        word_count < MIN_WORDS_FOR_VOCALS or
        speech_duration < MIN_SPEECH_DURATION
    )
    
    # Calculate confidence
    confidence = _calculate_confidence(
        word_count=word_count,
        speech_duration=speech_duration,
        has_speech=transcription.has_speech,
    )
    
    return InstrumentalResult(
        is_instrumental=is_instrumental,
        word_count=word_count,
        speech_duration=speech_duration,
        confidence=confidence,
    )


def _calculate_confidence(
    word_count: int,
    speech_duration: float,
    has_speech: bool,
) -> float:
    """
    Calculate confidence score for instrumental detection.
    
    Args:
        word_count: Number of words detected
        speech_duration: Duration of detected speech in seconds
        has_speech: Whether any speech was detected
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    if not has_speech:
        # No speech detected = high confidence
        return 0.95
    
    if word_count < 5:
        # Very few words = high confidence
        return 0.9
    
    if word_count < MIN_WORDS_FOR_VOCALS:
        # Below threshold = medium-high confidence
        return 0.8
    
    if speech_duration < MIN_SPEECH_DURATION:
        # Short speech duration = medium confidence
        return 0.7
    
    # Above thresholds = low confidence (likely has vocals)
    return 0.2
