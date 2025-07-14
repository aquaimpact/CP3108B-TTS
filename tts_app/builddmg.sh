#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/SpeechGen.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/SpeechGen.dmg" && rm "dist/SpeechGen.dmg"
create-dmg \
  --volname "SpeechGen" \
  --volicon "SpeechGen.icns" \
  --window-pos 100 100 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "SpeechGen.app" 175 120 \
  --hide-extension "SpeechGen.app" \
  --app-drop-link 425 120 \
  "dist/SpeechGen.dmg" \
  "dist/dmg/"