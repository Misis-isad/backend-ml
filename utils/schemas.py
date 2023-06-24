from pydantic import BaseModel


class MLTask(BaseModel):
    id: int
    status: str
    audio_filename: str
    video_filename: str
    text_filename: str
    text_fileurl: str
    result_filename: str


class RecordSettings(BaseModel):
    start_timecode: str
    end_timecode: str
    annotation_length: int
    article_length: int
    screenshot_timing: int


class RecordDto(BaseModel):
    video_link: str
    settings: RecordSettings
