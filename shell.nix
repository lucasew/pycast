{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    entr
    gnumake
    python3
  ];
  shellHook = ''
    if [ ! -d .venv ]; then
      make virtualenv
    fi
    . .venv/bin/activate
  '';
}
