"""Modal overlay for /help slash command and keyboard navigation guide."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from rich.text import Text
from substrate_onboarding.engine.commands import CommandRegistry


class HelpModal(ModalScreen[None]):
    """Floating modal overlay displaying slash commands and keyboard shortcuts."""

    BINDINGS = [
        ("escape", "dismiss", "Close Help"),
        ("q", "dismiss", "Close Help"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(classes="modal-dialog"):
            yield Label("⚡ AGENT SUBSTRATE NAVIGATION & COMMANDS", classes="modal-title")

            yield Label("Global Slash Commands:", classes="wizard-step-title")
            for cmd in CommandRegistry.get_command_list():
                t = Text()
                t.append(f"  {cmd.name.ljust(10)}", style="bold #5eead4")
                t.append(f"Aliases: {', '.join(cmd.aliases).ljust(14)}", style="#8b949e")
                t.append(f" {cmd.description}", style="#f0f6fc")
                yield Static(t)

            yield Label("\nKeyboard Navigation Shortcuts:", classes="wizard-step-title")
            shortcuts = [
                ("[Up / Down]", "Navigate items, options, and lists"),
                ("[Enter]", "Select option / Submit input / Proceed to next state"),
                ("[Space]", "Toggle selection or buttons"),
                ("[Tab / Shift+Tab]", "Move focus across interactive controls"),
                ("[Ctrl+C / Ctrl+D]", "Pause onboarding & prompt exit confirmation"),
                ("[Esc]", "Close modal dialogs"),
            ]
            for key, desc in shortcuts:
                t = Text()
                t.append(f"  {key.ljust(22)}", style="bold #c084fc")
                t.append(f"{desc}", style="#f0f6fc")
                yield Static(t)

            with Horizontal(classes="auth-button-row"):
                yield Button("Close (Esc)", id="btn-close-help", classes="secondary-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-close-help":
            self.dismiss()
