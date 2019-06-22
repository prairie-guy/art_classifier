# Art Classifier 
## [fast.ai](https://www.fast.ai) models on [Render](https://render.com)

This repo can be used as a starting point to deploy [fast.ai](https://github.com/fastai/fastai) models on Render.

The sample app described here is up at https://fastai-v3.onrender.com. Test it out with bear images!

You can test your changes locally by installing Docker and using the following command:

```
docker build -t fastai-v3 . && docker run --rm -it -p 5000:5000 fastai-v3
```

The guide for production deployment to Render is at https://course.fast.ai/deployment_render.html.

Please use [Render's fast.ai forum thread](https://forums.fast.ai/t/deployment-platform-render/33953) for questions and support.


## Steps for Deploying Deeplearning Apps on Render
- Used `Dropbox_Uploader` (https://github.com/andreafabrizi/Dropbox-Uploader.git) to load model to  Dropbox. Authorization are set up and saved in file: `~/.dropbox_uploader` 

- Dropbox path: `Apps/fastai_uploader_2345`

- Upload export.pk1 to dropbox App/fastai_uploader_2345/export1.pk1 
dropbox_uploader.sh upload export.pkl export_something.pk1

- Confirm file has been uploaded to Dropbox/Apps

- Select '...' and choose `Share/Show` Link and copy this link. 

- Paste link from Dropbox/Share to this site to generate a download link:
https://syncwithtech.blogspot.com/p/direct-download-link-generator.html

- Add new repository in Github/Respositories/New/Import_Repository

- git clone http:gitbub.com/prairie-guy/new_repo

- Edit new_repository/app/server.py to include Dropbox download link, classes and other customizations.

- Add a new app on http://Render.com as a WebService, link it to new github repo.

- Set up as Docker