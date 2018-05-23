UNAME := $(shell uname -s)

upload: clean
	@[ "$$(git symbolic-ref -q HEAD)" == "refs/heads/develop" ] || \
		{ echo "Uploading can only be done on the master branch."; exit 1; }
	python3 setup.py sdist && \
	if [ "$(UNAME)" = "Darwin" ]; then \
		open -g -a Docker && \
		until docker ps -q >/dev/null 2>/dev/null; do \
			sleep 1; \
		done; \
	fi; \
	docker build -t vimtips_build:latest -f Dockerfile_wheel_manylinux . && \
	docker run -d --name vimtips_build vimtips_build:latest sleep 600 && \
	docker cp vimtips_build:'/vimtips/dist' ./ && \
	docker kill vimtips_build && \
	docker rm vimtips_build; \
	if [ "$(UNAME)" = "Darwin" ]; then \
		python3 setup.py bdist_wheel; \
	fi; \
	true

clean:
	rm -rf build dist *.egg-info

.PHONY: clean upload
