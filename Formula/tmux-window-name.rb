class TmuxWindowName < Formula
  desc "Smart tmux window names like IDE tablines"
  homepage "https://github.com/leftrk/tmux-window-name"
  url "https://github.com/leftrk/tmux-window-name/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "SHA256_WILL_BE_CALCULATED_AFTER_TAG_RELEASE"
  license "MIT"
  head "https://github.com/leftrk/tmux-window-name.git", branch: "dev"

  depends_on "tmux"
  depends_on "python@3.11"

  def install
    # Create virtualenv and install the package
    venv = virtualenv_create(libexec, "python3.11")
    venv.pip_install(buildpath)

    # Install bash entry script
    libexec.install "tmux_window_name.tmux"
  end

  def caveats
    <<~EOS
      To enable this plugin, add to your ~/.tmux.conf:

        With TPM (recommended):
          set -g @plugin 'leftrk/tmux-window-name'

        Without TPM:
          run-shell #{libexec}/tmux_window_name.tmux

      Note: If using tmux-resurrect, load this plugin BEFORE it.
    EOS
  end

  test do
    assert_predicate libexec/"tmux_window_name.tmux", :exist?
    # Test that package is installed in virtualenv
    assert_predicate libexec/"lib/python3.11/site-packages/tmux_window_name/__init__.py", :exist?
  end
end