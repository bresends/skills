{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (ps: with ps; [
      playwright
      psycopg2
      python-dotenv
    ]))
    playwright-driver.browsers
  ];
}
