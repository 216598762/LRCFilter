"""Output writer module for writing results to files."""

from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional

from lrcfilter.config import OUTPUT_ENCODING, INCLUDE_TIMESTAMP
from lrcfilter.models import (
    AudioFile,
    CensorshipResult,
    InstrumentalResult,
    MismatchResult,
)


def write_results(
    censored_tracks: List[Tuple[AudioFile, CensorshipResult]],
    instrumental_tracks: List[Tuple[AudioFile, InstrumentalResult]],
    metadata_mismatches: List[Tuple[AudioFile, MismatchResult]],
    output_dir: Path,
) -> None:
    """
    Write all results to output files.
    
    Args:
        censored_tracks: List of (AudioFile, CensorshipResult) tuples
        instrumental_tracks: List of (AudioFile, InstrumentalResult) tuples
        metadata_mismatches: List of (AudioFile, MismatchResult) tuples
        output_dir: Directory to write output files
    """
    # Write censored tracks
    if censored_tracks:
        _write_censored_file(censored_tracks, output_dir)
    
    # Write instrumental tracks
    if instrumental_tracks:
        _write_instrumental_file(instrumental_tracks, output_dir)
    
    # Write metadata mismatches
    if metadata_mismatches:
        _write_mismatch_file(metadata_mismatches, output_dir)


def _write_censored_file(
    tracks: List[Tuple[AudioFile, CensorshipResult]],
    output_dir: Path,
) -> None:
    """
    Write censored tracks to file.
    
    Args:
        tracks: List of (AudioFile, CensorshipResult) tuples
        output_dir: Output directory
    """
    output_path = output_dir / "censored.txt"
    
    with open(output_path, "w", encoding=OUTPUT_ENCODING) as f:
        # Write header
        f.write("# Censored/Non-Explicit Tracks\n")
        if INCLUDE_TIMESTAMP:
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total: {len(tracks)} tracks\n")
        f.write("\n")
        
        # Write tracks
        for audio_file, result in tracks:
            f.write(f"{audio_file.path}\n")
            if result.details:
                f.write(f"  # {result.details}\n")
            f.write(f"  # Confidence: {result.confidence:.1%}\n")
            f.write("\n")
    
    print(f"  Written {len(tracks)} censored tracks to {output_path}")


def _write_instrumental_file(
    tracks: List[Tuple[AudioFile, InstrumentalResult]],
    output_dir: Path,
) -> None:
    """
    Write instrumental tracks to file.
    
    Args:
        tracks: List of (AudioFile, InstrumentalResult) tuples
        output_dir: Output directory
    """
    output_path = output_dir / "instrumental.txt"
    
    with open(output_path, "w", encoding=OUTPUT_ENCODING) as f:
        # Write header
        f.write("# Instrumental Tracks (No Vocals)\n")
        if INCLUDE_TIMESTAMP:
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total: {len(tracks)} tracks\n")
        f.write("\n")
        
        # Write tracks
        for audio_file, result in tracks:
            f.write(f"{audio_file.path}\n")
            f.write(f"  # Words detected: {result.word_count}, Speech duration: {result.speech_duration:.1f}s\n")
            f.write(f"  # Confidence: {result.confidence:.1%}\n")
            f.write("\n")
    
    print(f"  Written {len(tracks)} instrumental tracks to {output_path}")


def _write_mismatch_file(
    tracks: List[Tuple[AudioFile, MismatchResult]],
    output_dir: Path,
) -> None:
    """
    Write metadata mismatches to file.
    
    Args:
        tracks: List of (AudioFile, MismatchResult) tuples
        output_dir: Output directory
    """
    output_path = output_dir / "metadata_mismatches.txt"
    
    with open(output_path, "w", encoding=OUTPUT_ENCODING) as f:
        # Write header
        f.write("# Metadata Mismatches\n")
        if INCLUDE_TIMESTAMP:
            f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total: {len(tracks)} tracks with mismatched metadata\n")
        f.write("\n")
        
        # Write tracks
        for audio_file, result in tracks:
            f.write(f"# File: {audio_file.path}\n")
            f.write(f"  {result.details}\n")
            f.write(f"  # Confidence: {result.confidence:.1%}\n")
            f.write("---\n")
    
    print(f"  Written {len(tracks)} metadata mismatches to {output_path}")
