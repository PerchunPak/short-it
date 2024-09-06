{
  description = "My personal link shorter adapted to my needs and special link structure!";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
    }:
    let
      all = flake-utils.lib.eachDefaultSystem (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system}.extend poetry2nix.overlays.default;
          short-it = pkgs.callPackage ./package.nix { };
        in
        {
          packages = {
            inherit short-it;
            default = short-it;
          };

          devShells.default = pkgs.mkShell {
            inputsFrom = [ short-it ];
            packages = [ pkgs.poetry ];
          };
        }
      );
    in
    {
      nixosModules.short-it = import ./module.nix;
      nixosModules.default = self.nixosModules.short-it;

      overlays.short-it = (final: prev: { short-it = all.packages.${prev.system}.default; });
      overlays.default = self.overlays.short-it;
    }
    // all;
}
