{
  config,
  lib,
  pkgs,
  ...
}:

let
  cfg = config.services.short-it;
  short-it = pkgs.callPackage ./package.nix { };
in
{
  options.services.short-it = {
    enable = lib.mkEnableOption "Enable short-it";

    package = lib.mkOption {
      type = lib.types.package;
      default = short-it;
    };

    datadir = lib.mkOption {
      type = lib.types.path;
      default = "/var/lib/my/short-it";
    };

    host = lib.mkOption {
      type = lib.types.str;
      default = "127.0.0.1";
    };
    port = lib.mkOption {
      type = lib.types.port;
      default = 3000;
    };
  };

  config.systemd.services = lib.mkIf cfg.enable {
    short-it = {
      enable = true;
      description = "My personal link shorter adapted to my needs and special link structure!";
      unitConfig.Type = "simple";
      script = "${cfg.package}/bin/short-it";
      serviceConfig = {
        User = "short-it";
        Group = "short-it";
        WorkingDirectory = cfg.datadir;
        Restart = "on-failure";
        RestartSec = "1s";
      };
      wantedBy = [ "multi-user.target" ];
    };
  };

  config.users = lib.mkIf cfg.enable {
    users.short-it = {
      isSystemUser = true;
      description = "short-it user";
      home = cfg.datadir;
      createHome = true;
      group = "short-it";
    };

    groups.short-it = { };
  };
}
