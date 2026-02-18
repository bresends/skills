{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (ps: with ps; [
      google-genai
      python-dotenv
      psycopg2
    ]))
  ];
}
