{ poetry2nix, ... }:
poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  checkGroups = [
    "make"
    "typing"
    "tests"
  ];

  checkPhase = ''
    runHook preCheck
    pytest --no-testmon
    runHook postCheck
  '';
}
