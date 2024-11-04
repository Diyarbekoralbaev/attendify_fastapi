from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import aiofiles
from pathlib import Path


image_handle_router = APIRouter(
    tags=['image_handle']
)

upload_folder = Path('test_camera')
upload_folder.mkdir(parents=True, exist_ok=True)


@image_handle_router.post('/upload')
async def upload_image(image: UploadFile = File(...)):
    try:
        image_path = upload_folder / image.filename

        try:
            file_content = await image.read()

            async with aiofiles.open(image_path, 'wb') as file:
                await file.write(file_content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {
            'status': 'success',
            'message': 'Image uploaded successfully',
        }
    except Exception as e:
        return {'detail': str(e)}