GCR_SITE=asia.gcr.io/jitta-dev/
APP_NAME=marketvaluation
APP_IMAGE=$(GCR_SITE)$(APP_NAME)
CLUSTER_DEV=dev-c3

# set project
set-project:
	gcloud config set project jitta-dev
use-dev-kube-config:
	gcloud config configurations activate jitta-dev
activate-interface:
	gcloud container clusters get-credentials $(CLUSTER_DEV) --zone=asia-east1-a
activate-project: set-project  use-dev-kube-config activate-interface


build:
	docker build --platform=linux/amd64 -t $(APP_IMAGE) .
push:
	docker push $(APP_IMAGE)
replace:
	sed 's,<image_name>,$(APP_IMAGE),g' ./kubernetes/${APP_NAME}-deployment.yaml | kubectl replace -f -
configmap:
	kubectl replace -f ./kubernetes/$(APP_NAME)-configmap.yaml
restart:
	kubectl delete pods -l name=$(APP_NAME)
delete:
	kubectl delete pod $(APP_NAME)
	
log:
	kubectl logs $(APP_NAME)



run-marketvaluation:
	kubectl run marketvaluation \
		--image=asia.gcr.io/jitta-dev/marketvaluation:latest \
		-- /bin/sh -c "pipenv run python loop_peband_monthly.py"


rerun: build push delete run-marketvaluation