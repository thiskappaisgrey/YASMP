{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  pname = "YASM";
  src = ./src;
  version = "0.1";
  propagatedBuildInputs = [ pkgs.python3Packages.flask ];
}
