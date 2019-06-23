import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles


################################################################################################
# BASIC CONFIGURATION
# soccer_or_football: version1
# export_file_name = 'export.pkl'
# export_file_url = 'https://www.dropbox.com/s/ky36nbjjjphfzor/export.pk1?dl=1'
# classes = ['soccer-player', 'football-player']#
#
# art_classifier: version 2
export_file_url = 'https://www.dropbox.com/s/fky9bmpy37e02ij/export_art_2.pkl?dl=1'
export_file_name = 'export_art_2.pkl'
classes =  ['Middle-Ages', 'Renaissance', 'Neoclassical', 'Impressionism', 'Cubism', 'Surrealism' ,'Pop-Art', 'Lowbrow', 'Abstract', 'Photorealism']
################################################################################################

path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())

################################################################
def to_percent(freq:tensor)->float:
    return round(float(f"{freq*100}"),2)

def get_prediction(im):
    cls = classes  # define above
    _,n,freq = learn.predict(im)
    freq = to_percent(freq[n])
    return f"{cls[n]} : {freq}%"
################################################################

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = get_prediction(img)
    return JSONResponse({'result': prediction})
    #prediction = learn.predict(img)[0]
    #return JSONResponse({'result': str(prediction)})

if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
