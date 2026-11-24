"""Atlas Order Services."""

import sys
import typing
from collections.abc import Callable
from typing import Any, cast

__version__ = "0.1.0"


if sys.version_info >= (3, 14):
    _typing_eval_type = cast(Callable[..., Any], getattr(typing, "_eval_type"))  # noqa: B009

    def _eval_type_compat(
        value: Any, globalns: dict[str, Any], localns: dict[str, Any], *args: Any, **kwargs: Any
    ) -> Any:
        kwargs.pop("prefer_fwd_module", None)
        return _typing_eval_type(value, globalns, localns, *args, **kwargs)

    setattr(typing, "_eval_type", _eval_type_compat)  # noqa: B010
