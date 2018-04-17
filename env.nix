with import <nixpkgs> {};

stdenv.mkDerivation rec {
    name = "confanalyz-env";

    nativeBuildInputs = with pythonPackages; [
        pymongo lxml
        (callPackage ./microdata.nix {})
    ];
}