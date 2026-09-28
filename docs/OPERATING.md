# Operating Instructions: LaBelle 202 LA Express

**LED programmable message display, operated with the LaBelle IR keyboard**

This guide is adapted from LaBelle's *INFO 152 Preliminary Operating
Instructions*. That manual was written for a sister model with a wired keypad,
but the 202 LA Express behaves largely the same way. Here the steps and
examples are rewritten for the keys of the **LaBelle IR keyboard**. They also
work from the `labelle-ir` web keyboard and command line, which send the same
codes. Where the 202 is known to differ from the INFO 152, that's noted. So
are details that haven't been confirmed on a 202 yet.

---

## Contents

1. [Conventions](#1-conventions)
2. [Using the keyboard](#2-using-the-keyboard)
3. [Keyboard operation](#3-keyboard-operation)
4. [Display functions](#4-display-functions)
5. [Graphics](#5-graphics)
6. [To enter a message](#6-to-enter-a-message)
7. [To run a message](#7-to-run-a-message)
8. [To edit a message](#8-to-edit-a-message)
9. [To set the time, day or date](#9-to-set-the-time-day-or-date)
10. [Other keyboard functions](#10-other-keyboard-functions)
11. [Differences from the INFO 152 manual](#11-differences-from-the-info-152-manual)
12. [Quick reference card](#12-quick-reference-card)

---

## 1. Conventions

| Written as | Means |
|---|---|
| **Run** | Press the key marked *Run* |
| **Control+New** | Hold **Control** and press the key with *New* printed above it (the *Run* key) |
| **Shift+4** | Hold **Shift** and press *4* (this types **$**) |
| **0 1** | Type the digits 0 then 1 |
| (space) | Press the space bar |
| *(Rot ← = H)* | The Control legend and the key it's printed above |

On the web keyboard, tap **Control** or **Shift** once and it applies to the
next key. Double-tap to lock it on.

> **Arrow keys in the `labelle-ir` tools.** The web app and command line swap
> the plain **←** and **→** keys, so the message moves in the direction the
> arrow points. **Control+← (Insert)**, **Control+→ (Delete)** and **Shift+←/→
> (↑/↓)** are not swapped. This guide describes what each arrow *does*
> (forward or back through the message), so follow the arrow's direction
> whichever keyboard you use.

## 2. Using the keyboard

1. Point the back edge of the keyboard directly at the sign.
2. Don't block the back edge of the keyboard.
3. Stay within about 30 feet of the sign for best results.
4. Replace the battery with a 9-volt alkaline when the red light on the back
   edge of the keyboard doesn't flash while you press **Run**. The battery is
   behind the side panel.

When using an IR gateway instead, the emitter must sit over the sign's IR
window: **13" from the left edge, about 5/8" below the top edge of the visible
display** on the 202 LA Express.

## 3. Keyboard operation

### Keys and legends

Each key can do up to three things:

| Layer | How to use it | Printed as |
|---|---|---|
| **Plain** | Press the key | The large character on the keycap |
| **Shift** | Hold **Shift**, press the key | The small character on the keycap (for example **$** on *4*, **↑** on *←*) |
| **Control** | Hold **Control**, press the key | The word printed **above** the key: **orange/red** = display functions, **blue** = editing and setup functions |

### Auto-repeat

Holding a character key, including the space bar, repeats that character. The
arrow keys and **Delete** also repeat while held. (On the web keyboard, keep
your finger on the key.)

## 4. Display functions

### Basics

A message is built from **phrases**. Each phrase starts with a **display
function** that controls how it appears. There are two kinds:

- **Rotate functions:** the phrase can be any length.
- **Screen functions:** the phrase can only be **one screenful** of
  characters.

Other functions change the phrase's characters or add live information:
**Wide**, **Speed**, and the clock/calendar functions **Time**, **Day** and
**Date**.

When you edit a message, display functions show up as two-letter codes. The
codes listed below are the ones the INFO 152 manual documents.

### Rotate functions (any length)

| Function | Key | INFO 152 code | Effect |
|---|---|---|---|
| Rotate left | **Control+Rot ←** *(H)* | RL | Message rotates from right to left across the screen |
| Rotate right | **Control+Rot →** *(J)* | RR | Message rotates from left to right across the screen |

### Screen functions (one screenful)

| Function | Key | INFO 152 code | Effect |
|---|---|---|---|
| Kick Off | **Control+Kick Off** *(M)* | KF | Message exits to the right one character at a time |
| Kick On | **Control+Kick On** *(N)* | KN | Message enters from the right one character at a time |
| Wipe | **Control+Wipe** *(P)* | WP | Message covers the preceding message from left to right |
| Open | **Control+Open** *(U)* | OP | Message expands from the centre of the display |
| Close | **Control+Close** *(I)* | CL | Message disappears into the centre of the display |
| Drop | **Control+Drop** *(L)* | DR | Preceding message drops down to reveal the new message |
| Scroll ↑ | **Control+Scroll ↑** *(V)* | SU | Message scrolls up from the bottom, pushing off the preceding message |
| Scroll ↓ | **Control+Scroll ↓** *(B)* | SD | Message scrolls down from the top, pushing off the preceding message |
| Blink | **Control+Blink** *(R)* | BL | Message blinks on and off six times, then holds for one second |
| Flash | **Control+Flash** *(E)* | FL | Message flashes three times, then holds for one second |
| Random | **Control+Random** *(Y)* | RM | Message appears one dot at a time as the preceding message disappears |
| Hold | *see note* | HL | Message is displayed for three seconds |
| Hold ↑ | *see note* | HU | Message is displayed for 1½ seconds, then moves up off the screen |
| Hold ↓ | *see note* | HD | Message is displayed for 1½ seconds, then moves down off the screen |

> **Note:** the IR keyboard has no key labelled *Hold*. **Control+Pause** *(Q)*
> is the likely equivalent, but this hasn't been confirmed on the 202.

The IR keyboard also has display functions that the INFO 152 manual doesn't
list: **Twinkle, Tear, Paint, Wiggle, Slide, Jaws, Swirl, Shoot** (Control+1
to 8), **Reverse** *(T)*, **Scan** *(O)* and **Instant** *(K)*. Use them the
same way as the screen functions above.

### Wide function

Wide shows characters at twice their normal width, to emphasise words or
phrases. While entering a message, press **Control+Wide** *(W)*. A small block
of LEDs lights in the upper-left corner of the screen to show that Wide is on.
Characters you type are now double width. Press **Control+Wide** again to
return to normal width.

### Clock and calendar functions

These show the time of day, the day of the week or the date inside a message.
The clock and calendar stop when power is lost, including when the power
supply is unplugged; see [section 9](#9-to-set-the-time-day-or-date).

| Function | Key | Displays |
|---|---|---|
| Time of day | **Control+Time** *(A)* | Hours and minutes with AM or PM, for example `12:45 PM` |
| Day of week | **Control+Day** *(S)* | `SUNDAY` through `SATURDAY`, padded to nine characters |
| Date | **Control+Date** *(D)* | Month and day, for example `DEC 25` |

### Speed function

Speed switches the display between normal and fast. While entering a message,
press **Control+Speed** *(Z)*. The display code **SF** confirms fast speed.
Press **Control+Speed** again to return to normal (slow) speed, shown as
**SS**.

## 5. Graphics

The sign has built-in graphic characters that can be added to any message.
Press **Control+Graphic** *(X)*, then type the **two-digit graphic number**.

The INFO 152 had ten graphics:

| INFO 152 | Graphic |
|---|---|
| G1 | Heart |
| G2 | Arrow up |
| G3 | Arrow down |
| G4 | Hollow arrow left |
| G5 | Hollow arrow right |
| G6 | Man |
| G7 | Automobile |
| G8 | Airplane |
| G9 | Semi truck |
| G0 | "Welcome" in script |

> The IR keyboard accepts graphic numbers **00 to 99**. The 202's numbering
> and set of graphics haven't been confirmed. Try the numbers and note which
> graphic each one shows.

## 6. To enter a message

### Basic steps

To change a message that's already stored, see [section 8](#8-to-edit-a-message).

1. Press **Control+New**. The sign asks which memory to use (`M??`).
2. Type the **two-digit memory number** (00–99). Any message already stored in
   that memory is erased.
3. Press the **display function** you want (Control plus a red key; see
   [section 4](#4-display-functions)).
4. Type the characters for that function. Remember that screen functions
   only show one screenful.
5. Repeat steps 3 and 4 until the message is finished.

### Examples

**Example 1: HELLO THERE**

| Step | Press | Notes |
|---|---|---|
| 1 | **Control+New** | Sign asks `M??` |
| 2 | **0 1** | Memory 01 |
| 3 | **Control+Rot ←** *(H)* | Rotate left |
| 4 | H E L L O (space) T H E R E | |
| 5 | (space) × one screen width | Scrolls the text fully off before it repeats. The INFO 152 used fifteen spaces for its 15-character display |
| 6 | **Run**, **0 1** | Runs memory 01 |

**Example 2: TODAY'S SPECIAL / ONIONS / $1.00 PER BAG / TODAY ONLY!**

| Step | Press | Notes |
|---|---|---|
| 1 | **Control+New** | |
| 2 | **0 2** | Memory 02 |
| 3 | **Control+Rot ←** *(H)* | |
| 4 | T O D A Y **Shift+-** S (space) S P E C I A L | **Shift+-** types the apostrophe |
| 5 | (space) × one screen width | |
| 6 | **Control+Open** *(U)* | |
| 7 | **Control+Wide** *(W)* | Wide on |
| 8 | O N I O N S | |
| 9 | **Shift+Space** | Half space on the INFO 152; unconfirmed on the 202 |
| 10 | **Control+Flash** *(E)* | |
| 11 | **Control+Wide** *(W)* | Wide off |
| 12 | **Shift+4** | Types **$** |
| 13 | 1 . 0 0 (space) P E R (space) B A G (space) | |
| 14 | **Control+Scroll ↑** *(V)* | |
| 15 | T O D A Y (space) O N L Y **Shift+1** (space) | **Shift+1** types **!** |
| 16 | **Shift+Space** | |
| 17 | **Control+Rot ←** *(H)* | |
| 18 | (space) × one screen width | |
| 19 | **Run**, **0 2** | |

**Example 3: WELCOME / TO THE PARTY / THE TIME IS / (time of day)**

| Step | Press | Notes |
|---|---|---|
| 1 | **Control+New** | |
| 2 | **0 3** | Memory 03 |
| 3 | **Control+Random** *(Y)* | |
| 4 | **Control+Graphic** *(X)*, then the "Welcome" graphic number | G0 on the INFO 152; see [section 5](#5-graphics) |
| 5 | (space) × 3 | |
| 6 | **Control+Kick Off** *(M)* | |
| 7 | **Control+Graphic** *(X)*, "Welcome" graphic number | |
| 8 | (space) × 3 | |
| 9 | **Control+Kick On** *(N)* | |
| 10 | T O (space) T H E (space) P A R T Y (space) | |
| 11 | **Control+Open** *(U)* | |
| 12 | T H E (space) T I M E (space) I S (space) (space) | |
| 13 | **Control+Random** *(Y)* | |
| 14 | **Control+Time** *(A)* | Inserts the time of day |
| 15 | (space) × 4 | |
| 16 | **Control+Close** *(I)* | |
| 17 | **Control+Time** *(A)* | |
| 18 | (space) × 4 | |
| 19 | **Run**, **0 3** | |

## 7. To run a message

### Basic steps

1. Enter the messages you want into memory (see [section 6](#6-to-enter-a-message)).
2. Press **Run**. The sign asks which memory (`M??`).
3. Type the **two-digit memory number**. That message starts running.
4. Repeat steps 2 and 3 to run a different message, or to restart the same
   one from the beginning.

### Example

First enter the examples from section 6.

| Step | Press | Result |
|---|---|---|
| 1 | **Run**, **0 1** | Message 01 starts running |
| 2 | **Run**, **0 1** | Message 01 restarts from the beginning |
| 3 | **Run**, **0 2** | Message 02 starts running |
| 4 | **Run**, **0 3** | Message 03 starts running |

## 8. To edit a message

### Basic steps

1. Press **Edit**. A running message stops at its current position.
2. Type the **two-digit memory number** of the message to edit.
3. Press **→** to move forward through the message.
4. Press **←** to move backward through the message.
5. Repeat steps 3 and 4 until the part to change is at the right edge of the
   screen.
6. **To insert** characters or display functions:
   - A. Press **Control+Insert** *(←)* to start insert mode. A small block of
     LEDs lights in the lower-left corner of the screen.
   - B. Type the characters and display functions to add.
   - C. Press **Control+Insert** again to stop insert mode. Anything typed
     after that **overwrites** the existing characters.
7. **To delete** characters or display functions:
   - A. Use the arrows to bring the unwanted character to the right edge of
     the screen.
   - B. Press **Control+Delete** *(→)* once for each character to remove. It
     repeats if held.
8. **To clear** the rest of a message, press **Control+Clear End** *(/)*. This
   erases everything from the current position to the end.

### Examples

First enter the examples from section 6.

**Example 1: change "HELLO THERE" to "HELLO MARGE" in message 01**

| Step | Press | Notes |
|---|---|---|
| 1 | **Edit** | The running message stops |
| 2 | **0 1** | Message 01 is ready to edit |
| 3 | **→** until the **O** of HELLO is at the right edge | |
| 4 | (space) | Overwrites the old space |
| 5 | M A R G E | Overwrites THERE |
| 6 | **Run**, **0 1** | |

**Example 2: change "ONIONS / $1.00 PER BAG / TODAY ONLY" to "APPLES / 10 CENTS EACH" in message 02**

| Step | Press | Notes |
|---|---|---|
| 1 | **Edit** | |
| 2 | **0 2** | |
| 3 | **→** until the **Open** function (`OP`) is at the right edge | |
| 4 | **Control+Wide** *(W)* | Wide on |
| 5 | A P P L E S | |
| 6 | **Shift+Space** | |
| 7 | **Control+Close** *(I)* | |
| 8 | A P P L E S | |
| 9 | **Shift+Space** | |
| 10 | **Control+Wide** *(W)* | Wide off |
| 11 | **Control+Blink** *(R)* | |
| 12 | 1 0 (space) C E N T S (space) E A C H (space) | |
| 13 | **Control+Random** *(Y)* | |
| 14 | (space) | |
| 15 | **Control+Clear End** *(/)* | Clears the rest of the old message |
| 16 | **Run**, **0 2** | |

**Example 3: change "THE" to "OUR" in message 03**

| Step | Press | Notes |
|---|---|---|
| 1 | **Edit** | |
| 2 | **0 3** | |
| 3 | **→** until **TO THE** is at the right edge | |
| 4 | **Control+Delete** *(→)* | Erases the E |
| 5 | **Control+Delete** | Erases the H |
| 6 | **Control+Delete** | Erases the T |
| 7 | **Control+Insert** *(←)* | Insert mode on |
| 8 | O U R | |
| 9 | **Run**, **0 3** | |

## 9. To set the time, day or date

The time, day and date can only be set while you're **entering or editing a
message** that contains them. If power is lost, the clock stops and has to be
set again.

> If messages or the time are lost every time the sign is unplugged, the
> internal backup battery is probably disconnected or worn out. See
> [Memory backup battery](../README.md#memory-backup-battery) in the README.

### Entering the value as digits

This is the method printed on the IR keyboard.

1. Press **Control+Time**, **Control+Day** or **Control+Date**.
2. **Time:** type 4 digits in 24-hour format, for example `2 1 0 0` = 9:00 PM.
3. **Day:** type 1 digit from 1 to 7, where 1 = Sunday.
4. **Date:** type 6 digits as MMDDYY, for example `1 2 0 6 8 8` = December 6, 1988.

### Adjusting a flashing field

This is the INFO 152 method.

1. With a message containing the time, day or date open for editing, use
   **←** and **→** to bring the time, day or date to the right edge of the
   screen. One field flashes: AM/PM, the day, or the date digits.
2. Hold **Shift** and press **↑** (Shift+←) or **↓** (Shift+→) to change the
   flashing value.
3. Press **←** or **→** to select the next field (minutes, then hours; or
   month) and repeat step 2.

### Example: set the time shown in message 03

| Step | Press | Notes |
|---|---|---|
| 1 | **Edit** | The running message stops |
| 2 | **0 3** | Message 03 is ready to edit |
| 3 | **←/→** to bring the time to the right edge | AM or PM is flashing |
| 4 | **Shift+↑** until AM/PM is correct | |
| 5 | **←** | The minutes flash |
| 6 | **Shift+↑** until the minutes are correct | |
| 7 | **←** | The hours flash |
| 8 | **Shift+↑** until the hour is correct | |
| 9 | **Run**, **0 3** | |

## 10. Other keyboard functions

These Control legends are on the IR keyboard, but the INFO 152 manual doesn't
cover them and their behaviour on the 202 isn't documented here:
**Memory** *(Edit)*, **Idle** *(F)*, **Center** *(G)*, **Tone** *(C)*,
**Schedule** *(;)*, **Options** *(,)*, **Demo** *(.)*, **Cap Lock** *(Lamp)*,
**Pause** *(Q)* and **F1–F4** *(9, 0, -, =)*.

## 11. Differences from the INFO 152 manual

**Established on the 202 LA Express (V5.0):**

| Topic | INFO 152 manual | 202 LA Express with the IR keyboard |
|---|---|---|
| Keypad | Wired keypad with a keyed connector | Infrared keyboard, 9 V battery |
| Second modifier key | **ALT** (gold legends) | **Control** (red and blue legends) |
| Choosing a memory | **ALT+M1** to **ALT+M5** (five memories) | Type a **two-digit** number after New, Run or Edit (sign shows `M??`) |
| Run | **RUN** restarts the last message | **Run** asks for a memory number |
| Edit | **SHIFT+EDIT** | Dedicated **Edit** key |
| Graphics | **ALT+G1** to **G0** (ten graphics) | **Control+Graphic** plus two digits (00–99) |
| Setting the clock | **SHIFT+↑** on a flashing field | Can also be typed as digits after Control+Time/Day/Date |
| Display functions | 16 functions | Adds Twinkle, Tear, Paint, Wiggle, Slide, Jaws, Swirl, Shoot, Reverse, Scan and Instant |

**Not yet confirmed on the 202:**

- Whether there's a Hold function, and whether **Control+Pause** is it.
- Whether **Shift+Space** is the half space.
- The graphic numbers and images.
- The display width in characters, and how many messages or characters the
  memory holds.
- The two-letter codes the 202 shows in edit mode.
- What the functions in [section 10](#10-other-keyboard-functions) do.

## 12. Quick reference card

This is transcribed from the instructions printed on the underside of the
LaBelle IR keyboard.

**Using the keyboard**
1. Point the back edge of the keyboard directly at the sign.
2. Don't block the back edge of the keyboard.
3. Stay within 30 feet of the sign for best results.
4. Replace the battery with a 9-volt alkaline when the red light on the back
   edge doesn't flash while you press **Run**.
5. See the manual for details.

**To enter a message**
1. Hold **Control**, press *New*.
2. Enter a two-digit memory number, 00–99.
3. Hold **Control** and select an orange display function (*Rotate*, *Tear*, and so on).
4. Enter the message for that function.
5. Repeat steps 3 and 4 until the whole message has been entered.

**To run a message**
1. Press **Run**.
2. Enter a two-digit memory number, 00–99.

**To set the time, day or date**
1. Hold **Control**, press *Time*, *Day* or *Date*.
2. To set *Time*, enter 4 digits in 24-hour format (2100 = 9:00 PM).
3. To set *Day*, enter 1 digit (1–7, 1 = Sunday).
4. To set *Date*, enter 6 digits (120688 = December 6, 1988).
5. You can use ← and → to select the flashing character, then hold **Shift**
   and use ↑ and ↓ to change the value.

**Display functions**
*Rot ←* and *Rot →* rotate the message left or right. All other (orange)
display functions are limited to one screenful of characters.

**To add graphics to a message**
1. Hold **Control**, press *Graphic*.
2. Select a two-digit graphic, 00–99.

**To edit a message**
1. Press **Edit**.
2. Select a two-digit memory number, 00–99.
3. Press → to move the message right.
4. Press ← to move the message left.
5. Stop at the place to be changed.
6. To insert one or more characters or commands:
   - A. Hold **Control**, press *Insert* to start insert mode.
   - B. Add the characters and/or commands.
   - C. Hold **Control**, press *Insert* to stop insert mode.
7. To delete characters or commands: hold **Control** and press *Delete* for
   each character to be deleted.
8. Hold **Control** and press *Clear End* to delete everything beyond the
   point where the message is stopped.

The battery is behind the side panel. See the owner's manual.
