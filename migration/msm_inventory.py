"""Hard-coded MSM post inventory from the design spec §8.

13 entries in total: 12 recoverable + 1 (aloittaminen) skip.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class MSMPost:
    slug: str
    title: str
    lang: str          # "en" | "fi"
    published: date
    notes: str = ""


INVENTORY: list[MSMPost] = [
    MSMPost("aloittaminen", "Muutostekniikat: Mitä haluan muuttaa?", "fi", date(2020, 1, 1),
            notes="No individual Wayback snapshot — handled out-of-band"),
    MSMPost("safe-changes",
            "Changing something while not making it worse: 7 rules of thumb",
            "en", date(2020, 1, 1)),
    MSMPost("motivaatio-on-tietolahde",
            "Muutostekniikat: Motivaatio on tietolähde", "fi", date(2020, 1, 7)),
    MSMPost("tekniikkalistaus", "123 tekniikkaa itsensä johtamiseen",
            "fi", date(2020, 1, 7)),
    MSMPost("antihauras", "Antihauras elämä", "fi", date(2020, 2, 11)),
    MSMPost("123-techniques", "123 techniques for self-management",
            "en", date(2020, 3, 1)),
    MSMPost("mindfulness-face",
            "Mindfulness for burning cities and viral pandemics",
            "en", date(2020, 3, 1)),
    MSMPost("decline-handshake", "How to decline a handshake",
            "en", date(2020, 3, 12)),
    MSMPost("itseohjautuvuus",
            "Itseohjautuvat kansalaiset, kriisinkestävä yhteiskunta",
            "fi", date(2020, 8, 18)),
    MSMPost("uncertainty",
            "When uncertainty makes decisions easier, not harder",
            "en", date(2020, 9, 15)),
    MSMPost("valmius",
            "Pandemia haastaa ajattelumme: Neljä kompastuskiveä torjuntapolulla",
            "fi", date(2021, 3, 7)),
    MSMPost("fasting-experiment", "A 14-day Fasting Experiment",
            "en", date(2021, 9, 13)),
    MSMPost("personal-change",
            "Lifestyle change is not a willpower issue",
            "en", date(2023, 2, 14),
            notes="Reposted Helsinki University interview — try helsinki.fi first"),
]
