"""
Basic video exporting example
"""
# separate creation from use
import pathlib
from typing import Protocol, Type
from dataclasses import dataclass


class VideoExporter(Protocol):
    """Basic representation of video exporting codec."""

    def prepare_export(self, video_data):
        """Prepares video data for exporting."""

    def do_export(self, folder: pathlib.Path):
        """Exports the video data to a folder."""


class LosslessVideoExporter:
    """Lossless video exporting codec."""

    def prepare_export(self, video_data):
        print("Preparing video data for lossless export.")

    def do_export(self, folder: pathlib.Path):
        print(f"Exporting video data in lossless format to {folder}.")


class H264BPVideoExporter:
    """H.264 video exporting codec with Baseline profile."""

    def prepare_export(self, video_data):
        print("Preparing video data for H.264 (Baseline) export.")

    def do_export(self, folder: pathlib.Path):
        print(f"Exporting video data in H.264 (Baseline) format to {folder}.")


class H264Hi422PVideoExporter:
    """H.264 video exporting codec with Hi422P profile (10-bit, 4:2:2 chroma sampling)."""

    def prepare_export(self, video_data):
        print("Preparing video data for H.264 (Hi422P) export.")

    def do_export(self, folder: pathlib.Path):
        print(f"Exporting video data in H.264 (Hi422P) format to {folder}.")


class AudioExporter(Protocol):
    """Basic representation of audio exporting codec."""

    def prepare_export(self, audio_data):
        """Prepares audio data for exporting."""

    def do_export(self, folder: pathlib.Path):
        """Exports the audio data to a folder."""


class AACAudioExporter:
    """AAC audio exporting codec."""

    def prepare_export(self, audio_data):
        print("Preparing audio data for AAC export.")

    def do_export(self, folder: pathlib.Path):
        print(f"Exporting audio data in AAC format to {folder}.")


class WAVAudioExporter:
    """WAV (lossless) audio exporting codec."""

    def prepare_export(self, audio_data):
        print("Preparing audio data for WAV export.")

    def do_export(self, folder: pathlib.Path):
        print(f"Exporting audio data in WAV format to {folder}.")


class ExporterFactory(Protocol):
    """
    Factory that represents a combination of video and audio codecs.
    The factory doesn't maintain any of the instances it creates.
    """

    def get_video_exporter(self) -> VideoExporter:
        """Returns a new video exporter belonging to this factory."""

    def get_audio_exporter(self) -> AudioExporter:
        """Returns a new audio exporter belonging to this factory."""


class FastExporter:
    """Factory aimed at providing a high speed, lower quality export."""

    def get_video_exporter(self) -> VideoExporter:
        return H264BPVideoExporter()

    def get_audio_exporter(self) -> AudioExporter:
        return AACAudioExporter()


class HighQualityExporter:
    """Factory aimed at providing a slower speed, high quality export."""

    def get_video_exporter(self) -> VideoExporter:
        return H264Hi422PVideoExporter()

    def get_audio_exporter(self) -> AudioExporter:
        return AACAudioExporter()


class MasterQualityExporter:
    """Factory aimed at providing a low speed, master quality export."""

    def get_video_exporter(self) -> VideoExporter:
        return LosslessVideoExporter()

    def get_audio_exporter(self) -> AudioExporter:
        return WAVAudioExporter()


@dataclass
class MediaExporter:
    video: VideoExporter
    audio: AudioExporter

@dataclass
class MediaExporterFactory:
    video_class: Type[VideoExporter]
    audio_class: Type[AudioExporter]

    def __call__(self) -> MediaExporter:
        return MediaExporter(self.video_class(), self.audio_class())


FACTORIES = {
    "low": MediaExporterFactory(H264BPVideoExporter, AACAudioExporter),
    "high": MediaExporterFactory(H264Hi422PVideoExporter, AACAudioExporter),
    "master": MediaExporterFactory(LosslessVideoExporter, WAVAudioExporter),
}

def read_factory() -> MediaExporterFactory:
    """Constructs an exporter factory based on the user's preference."""

    while True:
        export_quality = input(
            f"Enter desired output quality ({', '.join(FACTORIES)}): "
        )
        try:
            return FACTORIES[export_quality]
        except KeyError:
            print(f"Unknown output quality option: {export_quality}.")


def do_export(exporter: MediaExporter) -> None:
    """Main function."""

    # prepare the export
    exporter.video.prepare_export("placeholder_for_video_data")
    exporter.audio.prepare_export("placeholder_for_audio_data")

    # do the export
    folder = pathlib.Path("/usr/tmp/video")
    exporter.video.do_export(folder)
    exporter.audio.do_export(folder)


def main():
    # create the factory
    factory = read_factory()

    # use the factory to create the media exporter
    media_exporter = factory()

    # perform the exporting job
    do_export(media_exporter)


if __name__ == "__main__":
    main()
