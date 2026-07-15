"""CLI entry point for LRCFilter."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from lrcfilter.scanner import scan_audio_files
from lrcfilter.metadata import extract_metadata
from lrcfilter.lyrics import fetch_lyrics
from lrcfilter.analyzer import analyze_audio
from lrcfilter.censorship import detect_censorship
from lrcfilter.instrumental import detect_instrumental
from lrcfilter.mismatch import detect_metadata_mismatch
from lrcfilter.output import write_results
from lrcfilter.config import DEFAULT_MODEL, DEFAULT_DEVICE, DEFAULT_COMPUTE_TYPE


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="lrcfilter",
        description="Audio analysis tool for detecting censored/explicit content and instrumental tracks",
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan for audio files",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("."),
        help="Output directory for result files (default: current directory)",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Whisper model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--device",
        "-d",
        type=str,
        default=DEFAULT_DEVICE,
        choices=["cpu", "cuda"],
        help=f"Device to run Whisper on (default: {DEFAULT_DEVICE})",
    )
    parser.add_argument(
        "--compute-type",
        type=str,
        default=DEFAULT_COMPUTE_TYPE,
        help=f"Compute type for Whisper (default: {DEFAULT_COMPUTE_TYPE})",
    )
    parser.add_argument(
        "--genius-token",
        type=str,
        default=None,
        help="Genius API access token (or set GENIUS_ACCESS_TOKEN env var)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()

    if not args.directory.exists():
        print(f"Error: Directory '{args.directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    if not args.directory.is_dir():
        print(f"Error: '{args.directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scanning {args.directory} for audio files...")
    audio_files = scan_audio_files(args.directory)
    print(f"Found {len(audio_files)} audio files.")

    if not audio_files:
        print("No audio files found. Exiting.")
        return

    # Process each file
    censored_tracks = []
    instrumental_tracks = []
    metadata_mismatches = []

    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] Processing: {audio_file.filename}")

        # Extract metadata
        metadata = extract_metadata(audio_file)
        if args.verbose:
            print(f"  Metadata: {metadata}")

        # Fetch lyrics
        lyrics = fetch_lyrics(
            metadata,
            genius_token=args.genius_token,
        )
        if args.verbose:
            print(f"  Lyrics source: {lyrics.source if lyrics else 'None'}")

        # Check for metadata mismatch
        if lyrics:
            mismatch = detect_metadata_mismatch(metadata, lyrics)
            if mismatch.is_mismatch:
                print(f"  ⚠ Metadata mismatch detected: {mismatch.details}")
                metadata_mismatches.append((audio_file, mismatch))

        # Analyze audio with Whisper
        transcription = analyze_audio(
            audio_file,
            model_name=args.model,
            device=args.device,
            compute_type=args.compute_type,
        )
        if args.verbose:
            print(f"  Transcription: {transcription.text[:100]}...")

        # Detect censorship
        if lyrics and lyrics.plain_lyrics:
            censorship_result = detect_censorship(
                lyrics.plain_lyrics,
                transcription.text,
            )
            if censorship_result.is_censored:
                print(f"  🚫 Censored detected (confidence: {censorship_result.confidence:.2f})")
                censored_tracks.append((audio_file, censorship_result))

        # Detect instrumental
        instrumental_result = detect_instrumental(transcription)
        if instrumental_result.is_instrumental:
            print(f"  🎵 Instrumental detected (confidence: {instrumental_result.confidence:.2f})")
            instrumental_tracks.append((audio_file, instrumental_result))

    # Write results
    print("\n" + "=" * 50)
    print("Writing results...")
    write_results(
        censored_tracks=censored_tracks,
        instrumental_tracks=instrumental_tracks,
        metadata_mismatches=metadata_mismatches,
        output_dir=args.output_dir,
    )

    # Print summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Total files processed: {len(audio_files)}")
    print(f"  Censored/non-explicit: {len(censored_tracks)}")
    print(f"  Instrumental: {len(instrumental_tracks)}")
    print(f"  Metadata mismatches: {len(metadata_mismatches)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
