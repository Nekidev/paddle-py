uv version --bump patch
uv build
uv publish --username __token__
git add .
git commit -am "chore: publish new version"
git tag "$(uv version --short)"
git push origin main --tags
