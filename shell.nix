{ pkgs ? import <nixpkgs> {} }:
let
  myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    editablePackageSources = {
      my-app = ./src;
    };
  };
in
pkgs.mkShell {
  buildInputs = [
    myAppEnv
    pkgs.python3
    pkgs.poetry
    pkgs.sqlite
    # For Tailwindcss
    pkgs.nodejs
  ];
}
