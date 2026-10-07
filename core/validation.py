import ipaddress
import re


class TargetValidationError(ValueError):
    pass


def validate_ping_target(target: str) -> str:
    target = target.strip()

    if not target:
        raise TargetValidationError(
            "Ping target cannot be empty."
        )

    if len(target) > 253:
        raise TargetValidationError(
            "Ping target is too long."
        )

    # First check whether it is a valid IPv4/IPv6 address.
    try:
        ipaddress.ip_address(target)
        return target

    except ValueError:
        pass

    # If it is not an IP address, validate it as a hostname.
    if target.endswith("."):
        target = target[:-1]

    if not target:
        raise TargetValidationError(
            "Invalid hostname."
        )

    labels = target.split(".")

    hostname_pattern = re.compile(
        r"^[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
    )

    for label in labels:
        if not hostname_pattern.match(label):
            raise TargetValidationError(
                "Enter a valid IP address or hostname."
            )

    return target