import random
import weapons
random.seed()


def main(orig_ap, orig_hit, orig_crit, orig_exp, mh, oh, duration=60, total_sims=100):
    mh_name = mh
    mh = weapons.get_weapon_stats(mh_name)
    mh_bot, mh_top, orig_mh_speed = mh[0], mh[1], mh[2]
    oh_name = oh
    oh = weapons.get_weapon_stats(oh_name)
    oh_bot, oh_top, orig_oh_speed = oh[0], oh[1], oh[2]
    spell_hit_chance = 0.05
    spell_crit_chance = 0.042
    boss_armor = 6950

    # Set special weapons
    dragon_wep = False
    if mh_name == "Dragonmaw":
        dragon_wep = True

    def calc_time(hundredths):
        return round(hundredths / 100, 2)

    def melee_hit():
        return random.random() <= 0.72 + hit_chance

    def melee_dodge():
        return random.random() <= 0.9375 + expertise

    def melee_crit():
        return random.random() <= crit_chance

    def calc_dmg(ap, bot, top, speed):
        _crit = melee_crit()
        return (((random.randrange(bot, top) + (ap * speed / 14)) * (1 + int(_crit))) * 1.1) * \
               (1 - (boss_armor / (boss_armor + 10557.5))), int(_crit)

    def calc_wf_dmg(ap, bot, top, speed):
        wf1 = 0
        wf2 = 0
        crit1 = False
        crit2 = False
        if melee_dodge():
            wf1, crit1 = calc_dmg(ap, bot, top, speed)
        if melee_dodge():
            wf2, crit2 = calc_dmg(ap, bot, top, speed)
        return wf1 + wf2, int(crit1) + int(crit2)

    def spell_hit():
        return random.random() <= 0.84 + spell_hit_chance

    def spell_crit():
        return random.random() <= spell_crit_chance

    def cast_flame_shock(ap):
        return (377 + 0.214 * ap * 0.3) * (1 + int(spell_crit())) + 420 + 0.1 * 0.3

    def cast_earth_shock(ap):
        return (658 + 0.386 * ap * 0.3) * (1 + int(spell_crit()))

    def check_dragon_haste():
        return random.random() < 2.7 * 1.4 / 60

    def check_mongoose():
        return random.random() < 2.7 * 1.4 / 60

    def update_weapon_speeds(wep_speed, flurry_remaining, dragon, mh_mong, oh_mong):
        flurry = 0
        if flurry_remaining > 0:
            flurry = 0.3
        return wep_speed / (
                (1 + flurry) * (1 + int(dragon) * 0.1342) * (1 + int(mh_mong * 0.0188) * (1 + int(oh_mong * 0.0188))))

    def update_crit(mh_mong, oh_mong):
        return orig_crit + (120 / 25) * int(mh_mong) + (120 / 25) * int(oh_mong)

    # Damage categories for displaying and calculating with all total sims.
    total_mh_white = 0
    total_oh_white = 0
    total_mh_wf = 0
    total_oh_wf = 0
    total_ss = 0
    total_fs = 0
    total_es = 0

    for sim in range(total_sims):
        # Initializing variables for each sim.
        attack_power = orig_ap
        hit_chance = orig_hit / 100
        crit_chance = orig_crit / 100
        expertise = orig_exp * 0.0025
        mh_speed = orig_mh_speed
        oh_speed = orig_oh_speed
        last_mh_swing = -1 * mh_speed
        last_oh_swing = -1 * oh_speed
        last_wf = -3
        next_cast = 0
        last_ss = -10
        ss_cd = 10
        last_shock = -6
        shock_cd = 6
        last_fs = -12
        fs_cd = 12
        flurry_count = 0
        dragon_haste = False
        last_dragon_haste = -12
        mh_mongoose = False
        last_mh_mongoose = -15
        oh_mongoose = False
        last_oh_mongoose = -15
        unleashed_rage = False
        last_unleashed_rage = -10

        # Check to see if melee swings are up and check for hits, damage, windfury, and crits.
        for hundredth in range(duration * 100):
            time = calc_time(hundredth)
            crit_counter = 0
            if round(last_mh_swing + mh_speed, 2) == time:
                if flurry_count > 0 and time - last_oh_swing < 0.5:
                    flurry_count -= 1
                last_mh_swing = time
                if melee_hit() and melee_dodge():
                    if dragon_wep and check_dragon_haste():
                        dragon_haste = True
                        last_dragon_haste = time
                    if check_mongoose():
                        mh_mongoose = True
                        last_mh_mongoose = time
                        crit_chance = update_crit(mh_mongoose, oh_mongoose)
                    dmg, crit = calc_dmg(attack_power, mh_bot, mh_top, orig_mh_speed)
                    total_mh_white += dmg
                    crit_counter += crit
                    if last_wf + 3 <= time and random.random() <= 0.36:
                        last_wf = time
                        wf_dmg, crit = calc_wf_dmg(attack_power + 555, mh_bot, mh_top, orig_mh_speed)
                        total_mh_wf += wf_dmg
                        crit_counter += crit
            if round(last_oh_swing + oh_speed, 2) == time:
                if flurry_count > 0 and time - last_mh_swing < 0.5:
                    flurry_count -= 1
                last_oh_swing = time
                if melee_hit() and melee_dodge():
                    if check_mongoose():
                        oh_mongoose = True
                        last_mh_mongoose = time
                        crit_chance = update_crit(mh_mongoose, oh_mongoose)
                    dmg, crit = calc_dmg(attack_power, oh_bot, oh_top, orig_oh_speed)
                    total_oh_white += dmg / 2
                    crit_counter += crit
                    if last_wf + 3 <= time and random.random() <= 0.36:
                        last_wf = time
                        wf_dmg, crit = calc_wf_dmg(attack_power + 555, oh_bot, oh_top, orig_oh_speed)
                        total_oh_wf += wf_dmg / 2
                        crit_counter += crit

            # Check to see if spells are off cooldown and cast them.
            if next_cast <= time:
                if last_ss + ss_cd <= time:
                    last_ss = time
                    dmg, crit = calc_dmg(attack_power, mh_bot, mh_top, orig_mh_speed)
                    if dragon_wep and check_dragon_haste():
                        dragon_haste = True
                        last_dragon_haste = time
                    if check_mongoose():
                        mh_mongoose = True
                        last_mh_mongoose = time
                        crit_chance = update_crit(mh_mongoose, oh_mongoose)
                    total_ss += dmg
                    crit_counter += crit
                    if last_wf + 3 <= time and random.random() <= 0.36:
                        last_wf = time
                        wf_dmg, crit = calc_wf_dmg(attack_power + 555, mh_bot, mh_top, orig_mh_speed)
                        total_mh_wf += wf_dmg
                        crit_counter += crit
                    if check_mongoose():
                        oh_mongoose = True
                        last_mh_mongoose = time
                        crit_chance = update_crit(mh_mongoose, oh_mongoose)
                    dmg, crit = calc_dmg(attack_power, oh_bot, oh_top, orig_oh_speed)
                    total_ss += dmg / 2
                    crit_counter += crit
                    if last_wf + 3 <= time and random.random() <= 0.36:
                        last_wf = time
                        wf_dmg, crit = calc_wf_dmg(attack_power + 555, oh_bot, oh_top, orig_oh_speed)
                        total_oh_wf += wf_dmg / 2
                        crit_counter += crit
                elif last_shock + shock_cd <= time:
                    last_shock = time
                    if last_fs + fs_cd <= time:
                        if spell_hit():
                            last_fs = time
                            total_fs += cast_flame_shock(attack_power)
                    else:
                        if spell_hit():
                            total_es += cast_earth_shock(attack_power)

            # Update buffs for attack speed and attack power.
            if crit_counter > 0:
                flurry_count = 3
                if unleashed_rage is False and last_unleashed_rage + 10 == time:
                    attack_power *= 1.1
            if unleashed_rage and last_unleashed_rage + 10 < time:
                attack_power /= 1.1
            if last_dragon_haste + 12 == time:
                dragon_haste = False
            if last_mh_mongoose + 15 == time:
                mh_mongoose = False
            if last_oh_mongoose + 15 == time:
                oh_mongoose = False

            # Update weapon speeds.
            mh_speed = update_weapon_speeds(orig_mh_speed, flurry_count, dragon_haste, mh_mongoose, oh_mongoose)
            oh_speed = update_weapon_speeds(orig_oh_speed, flurry_count, dragon_haste, mh_mongoose, oh_mongoose)

    mh_white_dps = round(total_mh_white / (duration * total_sims))
    oh_white_dps = round(total_oh_white / (duration * total_sims))
    mh_wf_dps = round(total_mh_wf / (duration * total_sims))
    oh_wf_dps = round(total_oh_wf / (duration * total_sims))
    ss_dps = round(total_ss / (duration * total_sims))
    fs_dps = round(total_fs / (duration * total_sims))
    es_dps = round(total_es / (duration * total_sims))
    total_dps = mh_white_dps + oh_white_dps + mh_wf_dps + oh_wf_dps + ss_dps + fs_dps + es_dps

    return [mh_white_dps, oh_white_dps, mh_wf_dps, oh_wf_dps, ss_dps, fs_dps, es_dps, total_dps]
