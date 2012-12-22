#!/bin/bash

brew rm portaudio
rm /Library/Caches/Homebrew/portaudio-edit.tgz
rm pa_stable_v19_20111121-edit.tgz
tar czf pa_stable_v19_20111121-edit.tgz portaudio
cp /usr/local/Library/Formula/portaudio.rb /usr/local/Library/Formula/portaudio.rb.orig
cp portaudio.rb /usr/local/Library/Formula/portaudio.rb
brew install portaudio --verbose
