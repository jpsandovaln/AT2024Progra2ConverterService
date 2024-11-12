import os
import ffmpeg
from converters.converter import Converter

from converters.audio_to_audio.audio_exception import AudioConversionError
from converters.audio_to_audio.audio_options import AudioOptions


class AudioConverter(Converter):
    def __init__(self, audio_path):
        self.audio_path = audio_path
        super().__init__(audio_path)

    def convert(self, output_format='mp3', **kwargs):
        output_path = self._get_output_path(output_format)
        temp_output_path = self._get_temp_output_path(output_format)

        # Get the options
        options = self._get_audio_options(**kwargs)

        try:
            self._convert_audio(
                output_path, temp_output_path, output_format, options)
        except ffmpeg.Error as e:
            raise AudioConversionError(f"Algo falló en la conversión de audio: {
                                       e.stderr.decode()}", 500)
        else:
            return temp_output_path if self.extension == output_format else output_path

    def _get_output_path(self, output_format):
        # Generate output path for the converted file and change format
        output_file = os.path.splitext(os.path.basename(self.audio_path))[
            0] + '.' + output_format
        return os.path.join('outputs', 'audio_converted_outputs', output_file)

    def _get_temp_output_path(self, output_format):
        # Generate output path for the converted file and change format
        output_file = os.path.splitext(os.path.basename(self.audio_path))[
            0] + '_convert.' + output_format
        return os.path.join('outputs', 'audio_converted_outputs', output_file)

    def _convert_audio(self, output_path, temp_output_path, output_format, options):
        # Performs audio conversion using ffmpeg
        ffmpeg.input(self.audio_path).output(temp_output_path if self.extension ==
                                             output_format else output_path, **options).run(overwrite_output=True)

    def _get_audio_options(self, **kwargs):
        # Verifies that options have been built
        opt = AudioOptions.build_options_audio(**kwargs)
        if opt is None:
            raise AudioConversionError(
                "Error al construir opciones de audio", 500)
        return opt
