import pytest

from click.testing import CliRunner
from mock import patch, sentinel
from requests.exceptions import RequestException

from wallpapers.wallpapers import (
    download, download_wallpapers, prepare_filename,
    prepare_image_download_url, proper_dimensions, get_reddit_submissions,
)


def test_prepare_filename():
    assert prepare_filename('some/file/path.jpg') == 'path.jpg'


@pytest.mark.parametrize(
    'param_url,param_expected_filename',
    [
        ('http://www.fake-imgur-link.xx/image',
         'http://www.fake-imgur-link.xx/image.jpg'),
        ('http://www.fake-imgur-link.xx/image.jpg',
         'http://www.fake-imgur-link.xx/image.jpg'),
        ('http://www.fake-staticflickr-link.xx/photo.jpg',
         'http://www.fake-staticflickr-link.xx/photo.jpg'),
        ('http://www.fake-staticflickr-link.xx/photo',
         'http://www.fake-staticflickr-link.xx/photo.jpg'),
        ('http://not-recognized-site.xx/picture.jpg', None)
    ]
)
def test_prepare_image_download_url(param_url, param_expected_filename):
    assert prepare_image_download_url(param_url) == param_expected_filename


@pytest.fixture
def test_url():
    return 'http://some-fake-url.xx.xx'


@patch('wallpapers.wallpapers.requests.get', autospec=True)
def test_download(mock_get, test_url):
    mock_get.return_value.raw = 'test raw response'

    result = download(test_url)

    assert result == 'test raw response'
    mock_get.assert_called_once_with(test_url, stream=True)


@patch('wallpapers.wallpapers.requests.get', side_effect=RequestException)
def test_download_raises_error(mock_get, test_url):
    with pytest.raises(RequestException):
        download(test_url)


@pytest.mark.parametrize(
    'param_width, param_height, param_expected_result',
    [
        (2000, 1200, True),
        (1200, 800, False),
    ]
)
@patch('wallpapers.wallpapers.Image', autospec=True)
def test_proper_dimensions(
        mock_image, param_width, param_height, param_expected_result):
    mock_image.size = (param_width, param_height)
    assert proper_dimensions(1920, 1080, mock_image) == param_expected_result


@patch('wallpapers.wallpapers.Reddit')
def test_get_reddit_submissions(mock_reddit):
    submissions = get_reddit_submissions()

    mock_reddit.assert_called_once_with(
        user_agent='earthporn_wallpapers_downloader')
    mock_reddit.return_value.get_subreddit.assert_called_once_with('earthporn')


@patch('wallpapers.wallpapers.prepare_filename')
@patch('wallpapers.wallpapers.proper_dimensions', return_value=True)
@patch('wallpapers.wallpapers.Image', autospec=True)
@patch('wallpapers.wallpapers.download')
@patch('wallpapers.wallpapers.prepare_image_download_url')
@patch('wallpapers.wallpapers.get_reddit_submissions')
def test_download_wallpapers(
    mock_get_submissions, mock_prepare_download_url, mock_download,
        mock_image, mock_proper_dimensions, mock_prepare_filename
):
    mock_get_submissions.return_value = [sentinel]
    mock_prepare_filename.return_value = 'test_filename'

    runner = CliRunner()
    result = runner.invoke(
        download_wallpapers,
        ['--subreddit=test_subreddit', '--width=800', '--height=500']
    )

    assert not result.exception
    mock_get_submissions.assert_called_once_with('test_subreddit')
    mock_prepare_download_url.assert_called_once_with(sentinel.url)
    mock_download.assert_called_once_with(
        mock_prepare_download_url.return_value)
    mock_image.open.assert_called_once_with(mock_download.return_value)
    mock_image.open.return_value.save.assert_called_once_with(
        'test_filename', 'JPEG')
