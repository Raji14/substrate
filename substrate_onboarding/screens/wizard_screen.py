"""State 2: Guided Questionnaire (Personalization Wizard) with Google Material 3 Design."""

from __future__ import annotations

from typing import List
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Label, Static, Button
from rich.text import Text
from substrate_onboarding.config import (
    OnboardingStep,
    TRACK_OPTIONS,
    DATAPLANE_OPTIONS,
    SANDBOX_OPTIONS,
    OptionItem,
)
from substrate_onboarding.widgets.status_bar import TopHeader, BottomBar


class QuestionnaireScreen(Screen[None]):
    """State 2: Guided Questionnaire with arrow-key navigation and persistent tab bar."""

    BINDINGS = [
        ("up", "cursor_up", "Move Up"),
        ("k", "cursor_up", "Move Up"),
        ("down", "cursor_down", "Move Down"),
        ("j", "cursor_down", "Move Down"),
        ("enter", "select_and_next", "Confirm & Next"),
        ("space", "select_and_next", "Confirm & Next"),
        ("b", "previous_substep", "Back"),
    ]

    SUB_STEPS = [
        ("track", "Phase 2.1: Workload Architecture & Persona Target", "Select your role and multiplexing target for GKE worker pools & actor sessions:", TRACK_OPTIONS),
        ("dataplane", "Phase 2.2: WorkerPool Fleet & Dataplane Topology", "Select the worker fleet isolation boundary (MicroVM / gVisor) and proxy:", DATAPLANE_OPTIONS),
        ("sandbox", "Phase 2.3: Optimization & Image Pre-caching", "Select your image caching strategy (Local SSD / GCS Checkpointing):", SANDBOX_OPTIONS),
    ]

    def __init__(self, name: str = "questionnaire"):
        super().__init__(name=name)
        self.sub_step_idx = 0
        self.selected_indices = [0, 0, 0]
        self.current_cursor = 0

    @property
    def current_options(self) -> List[OptionItem]:
        return self.SUB_STEPS[self.sub_step_idx][3]

    def compose(self) -> ComposeResult:
        yield TopHeader(initial_step=OnboardingStep.QUESTIONNAIRE)
        with Vertical(id="screen-container"):
            with Vertical(id="wizard-box"):
                yield Label("🛠️  STEP 2: PLATFORM SETUP & WORKERPOOL TOPOLOGY", classes="wizard-step-title", id="wizard-main-title")
                yield Label("", classes="wizard-step-title", id="wizard-sub-title")
                yield Label("", classes="wizard-step-subtitle", id="wizard-sub-desc")

                with Vertical(id="options-container"):
                    for i in range(5):
                        yield Static("", id=f"opt-card-{i}", classes="option-card")

                with Horizontal(classes="auth-button-row"):
                    btn_back = Button("← Back (b)", id="btn-wizard-back", classes="secondary-button")
                    btn_back.can_focus = False
                    yield btn_back

                    btn_skip = Button("Skip to Defaults (/skip)", id="btn-wizard-skip", classes="secondary-button")
                    btn_skip.can_focus = False
                    yield btn_skip

                    btn_next = Button("Next Step (Enter) →", id="btn-wizard-next", classes="action-button")
                    btn_next.can_focus = False
                    yield btn_next
        yield BottomBar(
            initial_tip="Choose your agent topology for GKE worker pools & multiplexing density.",
            initial_hints="[↑/↓] Select  [Enter] Next  [/skip] Defaults",
        )

    def on_mount(self) -> None:
        self._refresh_options_ui()

    def _refresh_options_ui(self) -> None:
        key, title, desc, options = self.SUB_STEPS[self.sub_step_idx]

        # Step indicator dots (e.g. ● ○ ○)
        dots = "".join(["● " if i == self.sub_step_idx else "○ " for i in range(len(self.SUB_STEPS))]).strip()
        step_header = Text()
        step_header.append(f"🛠️  {title}  ", style="bold #a8c7fa")
        step_header.append(f"[{dots}]", style="bold #81c995")

        # Update headers
        try:
            sub_title_lbl = self.query_one("#wizard-sub-title", Label)
            sub_title_lbl.update(step_header)
            sub_desc_lbl = self.query_one("#wizard-sub-desc", Label)
            sub_desc_lbl.update(desc)
        except Exception:
            pass

        # Update options cards with clear spacing and badges
        for i in range(5):
            try:
                card = self.query_one(f"#opt-card-{i}", Static)
                if i < len(options):
                    opt = options[i]
                    is_active = (i == self.current_cursor)

                    card.display = True
                    card.set_class(is_active, "-active")

                    t = Text()
                    if is_active:
                        t.append(" ▶ ", style="bold #a8c7fa")
                        t.append(f"{opt.icon}  {opt.title}", style="bold #ffffff")
                        if i == 0:
                            t.append("  [★ RECOMMENDED]", style="bold #fdd663 on #332a00")
                        t.append(f"\n     ↳ {opt.description}", style="#d3e3fd")
                    else:
                        t.append("   ", style="#9aa0a6")
                        t.append(f"{opt.icon}  {opt.title}", style="#f2f2f2")
                        if i == 0:
                            t.append("  [RECOMMENDED]", style="#fdd663")
                        t.append(f"\n     ↳ {opt.description}", style="#9aa0a6")

                    card.update(t)
                else:
                    card.display = False
            except Exception:
                pass

        # Update dynamic status bar tip on bottom border
        if 0 <= self.current_cursor < len(options):
            hovered_opt = options[self.current_cursor]
            try:
                bottom = self.query_one(BottomBar)
                bottom.set_tip(hovered_opt.tip)
                bottom.set_hints(f"[↑/↓] Select ({self.current_cursor + 1}/{len(options)})  [Enter] Next  [/skip] Defaults")
            except Exception:
                pass

    def action_cursor_up(self) -> None:
        if self.current_cursor > 0:
            self.current_cursor -= 1
            self._refresh_options_ui()

    def action_cursor_down(self) -> None:
        if self.current_cursor < len(self.current_options) - 1:
            self.current_cursor += 1
            self._refresh_options_ui()

    def action_select_and_next(self) -> None:
        self._commit_current_selection()
        if self.sub_step_idx < len(self.SUB_STEPS) - 1:
            self.sub_step_idx += 1
            self.current_cursor = self.selected_indices[self.sub_step_idx]
            self._refresh_options_ui()
        else:
            if hasattr(self.app, "advance_step"):
                self.app.advance_step()

    def _commit_current_selection(self) -> None:
        self.selected_indices[self.sub_step_idx] = self.current_cursor
        opt = self.current_options[self.current_cursor]

        if hasattr(self.app, "state"):
            if self.sub_step_idx == 0:
                self.app.state.track = opt.id
            elif self.sub_step_idx == 1:
                self.app.state.dataplane = opt.id
            elif self.sub_step_idx == 2:
                self.app.state.sandbox_tier = opt.id

    def action_previous_substep(self) -> None:
        if self.sub_step_idx > 0:
            self.sub_step_idx -= 1
            self.current_cursor = self.selected_indices[self.sub_step_idx]
            self._refresh_options_ui()
        else:
            if hasattr(self.app, "previous_step"):
                self.app.previous_step()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-wizard-next":
            self.action_select_and_next()
        elif event.button.id == "btn-wizard-back":
            self.action_previous_substep()
        elif event.button.id == "btn-wizard-skip":
            if hasattr(self.app, "advance_step"):
                self.app.advance_step()
