from io import BytesIO
from pathlib import Path
from shutil import rmtree

import pytest
from httpx import AsyncClient
from utils.settings import MEDIA_PATH

from .conftest import TEST_USERNAME


@pytest.fixture(scope="class")
def temp_media_dir(request):
    """Clean up of folder media"""
    test_user_media_path = MEDIA_PATH / TEST_USERNAME
    Path(test_user_media_path).mkdir(parents=True, exist_ok=True)
    yield test_user_media_path
    rmtree(test_user_media_path)


class TestMediaAPI:
    @classmethod
    def setup_class(cls):
        image_content = b"test"
        image_file = BytesIO(image_content)
        cls.files = {"file": ("image.jpg", image_file)}
        cls.invalid_files = {"file": ("image.jpg")}
        cls.base_url = "/medias"
        cls.test_user_media_path = MEDIA_PATH / TEST_USERNAME

    @pytest.mark.asyncio
    async def test_media_route(self, client: AsyncClient, temp_media_dir):
        if hasattr(self, "base_url") and hasattr(self, "files"):
            response = await client.post(self.base_url, files=self.files)

            assert response.status_code == 201
            assert response.json() == {"result": True, "media_id": 1}

    @pytest.mark.asyncio
    async def test_incorrect_api_key(self, client: AsyncClient):
        if hasattr(self, "base_url") and hasattr(self, "files"):
            headers = {"api-key": "RMTREE"}
            response = await client.post(
                self.base_url, headers=headers, files=self.files
            )
            assert response.status_code == 401
