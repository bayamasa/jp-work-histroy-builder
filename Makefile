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

# 職務経歴書（標準） - YAML=入力ファイル, CRED=個人情報ファイル, OUTPUT=出力ファイル
build-wh-standard:
	uv run python -m jp_tenshoku_docs_builder $(YAML) -c $(CRED) -o $(OUTPUT)

# 職務経歴書（STAR法） - YAML=入力ファイル, CRED=個人情報ファイル, OUTPUT=出力ファイル
build-wh-star:
	uv run python -m jp_tenshoku_docs_builder $(YAML) -c $(CRED) -o $(OUTPUT) --format star

# 履歴書 - YAML=入力ファイル, CRED=個人情報ファイル, OUTPUT=出力ファイル
build-resume:
	uv run python -m jp_tenshoku_docs_builder $(YAML) -c $(CRED) -o $(OUTPUT) --type resume

# サンプルPDF生成
sample-wh-standard:
	@mkdir -p output
	$(MAKE) build-wh-standard YAML=sample/work_history_standard.yaml CRED=sample/credential.yaml OUTPUT=output/work-history-standard.pdf

sample-wh-star:
	@mkdir -p output
	$(MAKE) build-wh-star YAML=sample/work_history_star.yaml CRED=sample/credential.yaml OUTPUT=output/work-history-star.pdf

sample-resume:
	@mkdir -p output
	$(MAKE) build-resume YAML=sample/resume.yaml CRED=sample/credential.yaml OUTPUT=output/resume.pdf

# Docker
docker-build:
	docker build -t jp-tenshoku-docs-builder .

docker-run-wh-standard: docker-build
	docker run --rm -v "$(PWD)":/work jp-tenshoku-docs-builder /work/sample/work_history_standard.yaml -c /work/sample/credential.yaml -o /work/output/work-history-standard.pdf

docker-run-wh-star: docker-build
	docker run --rm -v "$(PWD)":/work jp-tenshoku-docs-builder /work/sample/work_history_star.yaml -c /work/sample/credential.yaml -o /work/output/work-history-star.pdf --format star

docker-run-resume: docker-build
	docker run --rm -v "$(PWD)":/work jp-tenshoku-docs-builder /work/sample/resume.yaml -c /work/sample/credential.yaml -o /work/output/resume.pdf --type resume

# クリーンアップ
clean:
	rm -rf output/
