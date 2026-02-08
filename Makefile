.PHONY: setup test lint build-wh-standard build-wh-star build-resume sample-wh-standard sample-wh-star sample-resume clean docker-build docker-run-wh-standard docker-run-wh-star docker-run-resume

# セットアップ
setup:
	uv sync

# テスト
test:
	uv run pytest tests/ -v

# リント
lint:
	uv run ruff check src/ tests/

# 職務経歴書（標準） - YAML=入力ファイル, OUTPUT=出力ファイル
build-wh-standard:
	uv run python -m jb_workhistory $(YAML) -o $(OUTPUT)

# 職務経歴書（STAR法） - YAML=入力ファイル, OUTPUT=出力ファイル
build-wh-star:
	uv run python -m jb_workhistory $(YAML) -o $(OUTPUT) --format star

# 履歴書 - YAML=入力ファイル, OUTPUT=出力ファイル
build-resume:
	uv run python -m jb_workhistory $(YAML) -o $(OUTPUT) --type resume

# サンプルPDF生成
sample-wh-standard:
	$(MAKE) build-wh-standard YAML=sample/work_history_standard.yaml OUTPUT=work-history-standard.pdf

sample-wh-star:
	$(MAKE) build-wh-star YAML=sample/work_history_star.yaml OUTPUT=work-history-star.pdf

sample-resume:
	$(MAKE) build-resume YAML=sample/resume.yaml OUTPUT=resume.pdf

# Docker
docker-build:
	docker build -t jb-workhistory .

docker-run-wh-standard: docker-build
	docker run --rm -v "$(PWD)":/work jb-workhistory /work/sample/work_history_standard.yaml -o /work/work-history-standard.pdf

docker-run-wh-star: docker-build
	docker run --rm -v "$(PWD)":/work jb-workhistory /work/sample/work_history_star.yaml -o /work/work-history-star.pdf --format star

docker-run-resume: docker-build
	docker run --rm -v "$(PWD)":/work jb-workhistory /work/sample/resume.yaml -o /work/resume.pdf --type resume

# クリーンアップ
clean:
	rm -f work-history-standard.pdf work-history-star.pdf resume.pdf
