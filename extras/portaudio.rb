require 'formula'

class Portaudio < Formula
  homepage 'http://www.portaudio.com'
  url 'file:///Users/elijah/Development/portaudio-ctypes/extras/pa_stable_v19_20111121-edit.tgz'  #'http://www.portaudio.com/archives/pa_stable_v19_20111121.tgz'
  sha1 ''

  depends_on 'pkg-config' => :build

  option :universal

  fails_with :llvm do
    build 2334
  end

  # Fix PyAudio compilation on Lion
  def patches
    { :p0 =>
      "https://trac.macports.org/export/94150/trunk/dports/audio/portaudio/files/patch-include__pa_mac_core.h.diff"
    }
  end if MacOS.version >= :lion

  def install
    ENV.universal_binary if build.universal?

    args = [ "--prefix=#{prefix}",
             "--disable-debug", 
             "--disable-dependency-tracking",
            # "--enable-mac-debug=yes",
             # portaudio builds universal unless told not to
             "--enable-mac-universal=#{build.universal? ? 'yes' : 'no'}" ]

    system "./configure", *args
    system "make clean && make install"

    # Need 'pa_mac_core.h' to compile PyAudio
    include.install "include/pa_mac_core.h"
  end
end
