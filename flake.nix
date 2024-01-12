{
  description = "Python development environment";

  # Flake inputs
  inputs = {
    #nixpkgs.url = "nixpkgs/nixos-unstable";
    #flake-compat.url = "https://flakehub.com/f/edolstra/flake-compat/*.tar.gz";
    #flake-schemas.url = "https://flakehub.com/f/DeterminateSystems/flake-schemas/*.tar.gz";
    #nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/*.tar.gz";
    #nixpkgs.url = "github:domenkozar/nixpkgs/cpython-moduralize";
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.2305.491812.tar.gz";
  };

  # Flake outputs
  outputs = { self, nixpkgs }:
    let
      # Systems supported
      allSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      # Helper to provide system-specific attributes
      forAllSystems = f: nixpkgs.lib.genAttrs allSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      # Development environment output
      devShells = forAllSystems ({ pkgs }: {
        default =
          let
            # Use Python 3.11
            python = pkgs.python311;
          in
          pkgs.mkShell {
            # The Nix packages provided in the environment
            packages = [
              # Python plus helper tools
              (python.withPackages (ps: with ps; [
                virtualenv # Virtualenv
                pip # The pip installer
              ]))
            ];
          };
      });
      # TODO bind with devenvshellrc
       shellHook = ''
       pip install -r requirements.txt
       source .venv/bin/activate
       '';
    };
}

