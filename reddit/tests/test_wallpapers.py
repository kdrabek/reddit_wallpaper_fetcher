import pytest
import mock

from requests.exceptions import RequestException

from wallpapers.wallpapers import (
    download, prepare_filename, prepare_image_download_url, proper_dimensions,
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


@mock.patch('wallpapers.wallpapers.requests.get', autospec=True)
def test_download(mock_get, test_url):
    mock_get.return_value.raw = 'test raw response'

    result = download(test_url)

    assert result == 'test raw response'
    mock_get.assert_called_once_with(test_url, stream=True)


@mock.patch(
    'wallpapers.wallpapers.requests.get', side_effect=RequestException)
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
@mock.patch('wallpapers.wallpapers.Image', autospec=True)
def test_proper_dimensions(
    mock_image, param_width, param_height, param_expected_result):
    mock_image.size = (param_width, param_height)
    assert proper_dimensions(1920, 1080, mock_image) == param_expected_result
