# -*- coding: utf-8 -*-
"""Build a plain-language treatment guide for every symptom-weights row.

Educational support only. Not a personal prescription. Doses are left to a
clinician because they depend on pregnancy, clots, kidneys, allergies, and
other medicines.
"""
import csv
from pathlib import Path

SRC = Path(__file__).with_name("symptom-weights.csv")
OUT = Path(__file__).with_name("treatment-guides.csv")

DISEASE = {
    "PCOS": (
        "See a doctor to confirm PCOS and to rule out pregnancy, thyroid disease, and other causes of irregular periods. Ask for checks of blood sugar, cholesterol, and blood pressure.",
        "If you are not trying to get pregnant, a prescribed hormonal contraceptive or a progestin can bring regular bleeding and protect the uterine lining. Metformin is sometimes added for insulin resistance.",
        "If you are trying to get pregnant, letrozole is the usual first medicine to start ovulation. Daily activity and meals that steady blood sugar support cycles and long-term health.",
    ),
    "Endometriosis": (
        "Anti-inflammatory pain tablets, if they are safe for you, plus a heat pack, are the usual first help for period pain.",
        "Hormone treatment that limits periods — a continuous birth-control pill, a progestin, or a hormone IUD — is the usual medicine plan. GnRH medicines are a later option a specialist prescribes.",
        "If pain stays severe or pregnancy is not happening, a specialist may discuss laparoscopy to look for and remove endometriosis. Pelvic-floor physical therapy helps many people with ongoing pain.",
    ),
    "Uterine Fibroids": (
        "Medicines that lighten bleeding — tranexamic acid, an anti-inflammatory, a hormonal contraceptive, or a hormone IUD — are paired with iron if a blood count shows anemia.",
        "A doctor may use a time-limited hormone medicine to shrink bulk and ease pressure when fibroids are large.",
        "If bleeding, pressure, or pregnancy plans are not solved by medicine, procedures include embolization, fibroid removal, or hysterectomy. The choice depends on where the fibroid sits and whether you want a future pregnancy.",
    ),
    "Heavy Periods": (
        "On heavy days, tranexamic acid or an anti-inflammatory such as ibuprofen, if safe for you, can reduce flow. A doctor should confirm which one fits you, especially if you have ever had a blood clot.",
        "A hormone IUD, birth-control pills, or a progestin treats heavy bleeding over the following cycles. A blood count and iron test look for anemia.",
        "An ultrasound looks for fibroids, polyps, and other causes. Soaking protection every hour, fainting, or chest symptoms needs same-day care.",
    ),
    "Urinary Tract Infection": (
        "Get a urine test and finish the antibiotic a clinician chooses. Do not use leftover antibiotics.",
        "Drink water through the day. A short course of a urinary pain reliever such as phenazopyridine can ease burning if a pharmacist or doctor agrees. It turns urine orange and does not cure the infection.",
        "Fever, pain in the side or back, vomiting, pregnancy, or new confusion needs same-day care for a possible kidney infection.",
    ),
    "Yeast Infection": (
        "When yeast is confirmed, an azole cream or suppository from the pharmacy, or a single fluconazole tablet if a pharmacist or doctor says it is suitable, is standard treatment.",
        "Wear loose cotton underwear, skip scented washes, and finish the full course even after the itch fades.",
        "In pregnancy, the first time, or when itch keeps returning, get an exam. Oral fluconazole is avoided in pregnancy. Repeated yeast is a reason to check blood sugar.",
    ),
    "Bacterial Vaginosis": (
        "A prescribed antibiotic, usually metronidazole or clindamycin, clears bacterial vaginosis. Yeast cream does not.",
        "Do not douche or use scented vaginal products. Follow the alcohol warning on a metronidazole label.",
        "If the odor returns, get another swab rather than repeating random treatments. A clinician may use a longer course and will say whether a partner needs care.",
    ),
    "Pelvic Inflammatory Disease": (
        "Go to a clinic or emergency department the same day. This infection is treated with combination antibiotics after an exam, not with home remedies.",
        "Finish every dose, rest, and return quickly if pain, fever, or vomiting gets worse. Severe illness may need hospital care.",
        "Recent sexual partners need testing and treatment. Delay raises the risk of an abscess and later trouble getting pregnant.",
    ),
    "Menopause": (
        "Menopausal hormone therapy, when a doctor finds it safe for you, is the most effective treatment for hot flashes and night sweats and also helps bones and vaginal dryness.",
        "When hormones are not used, options include certain antidepressants, gabapentin, fezolinetant, cognitive behavioral therapy, a cooler bedroom, and less alcohol and caffeine.",
        "Vaginal moisturizers, lubricants, and low-dose vaginal estrogen treat dryness and pain with sex. Any bleeding after 12 months without a period needs a prompt exam.",
    ),
    "Osteoporosis": (
        "A bone-density scan, read with your fall risk and any past fracture, confirms osteoporosis and guides treatment strength.",
        "Get calcium mainly from food, take vitamin D if a test is low, do weight-bearing and strengthening exercise, and cut smoking and heavy alcohol. Make the home safer to prevent falls.",
        "After a fracture, or when fracture risk is high, a prescribed bone medicine such as a bisphosphonate lowers the chance of another break. A new fracture needs urgent bone care.",
    ),
    "Ovarian Cysts": (
        "Many simple cysts are watched with a repeat ultrasound because they shrink. Your doctor sets the timing.",
        "A heat pack and an anti-inflammatory pain tablet, if safe for you, can ease a mild ache while you wait for that plan.",
        "Sudden severe pain, fainting, vomiting, or shoulder-tip pain needs the emergency department to rule out torsion, rupture, or ectopic pregnancy.",
    ),
    "Cervical Screening": (
        "Attend Pap and HPV screening on schedule even when you feel well. Screening finds cell changes before cancer.",
        "If a result is abnormal, complete the repeat test or colposcopy in the letter. Do not skip it and do not start treatment on your own.",
        "Bleeding after sex, between periods, or after menopause needs a prompt visit and is not a reason to wait for the next routine screen. HPV vaccination is worthwhile if you are still eligible.",
    ),
    "Breast Screening": (
        "Have mammograms on the schedule for your age and risk, and bring earlier images if you can.",
        "A new lump, skin dimpling, a newly pulled-in nipple, or bloody nipple discharge needs diagnostic imaging now, not the next screening year.",
        "A callback usually means more pictures or an ultrasound. Biopsy follows only if those stay concerning. A red, hot, painful breast with fever needs same-day care.",
    ),
    "Thyroid Disorder": (
        "A TSH blood test, often with free T4, shows whether the thyroid is underactive or overactive.",
        "An underactive thyroid is treated with levothyroxine, with the dose set by follow-up blood tests. An overactive thyroid is treated with antithyroid medicine, radioactive iodine, or surgery. A beta blocker may slow a racing heart.",
        "A neck lump needs an ultrasound and sometimes a needle biopsy. Do not start iodine supplements or thyroid pills on your own.",
    ),
    "Iron-Deficiency Anemia": (
        "A blood count and ferritin confirm low iron. The doctor looks for the cause: often heavy periods, sometimes gut bleeding, low intake, or pregnancy.",
        "Take prescribed oral iron, or intravenous iron if tablets fail. Separate iron from thyroid medicine, tea, and coffee. A vitamin C-rich food with the dose helps absorption. Keep iron tablets away from children.",
        "Treat the cause or the anemia returns. Black tarry stools, chest pain, fainting, or severe breathlessness needs urgent care.",
    ),
    "Gestational Diabetes": (
        "Meet a pregnancy dietitian, check glucose as instructed, and do activity your obstetric clinician has approved.",
        "If glucose stays above target, your pregnancy team adds insulin or another medicine used in pregnancy. Do not start diabetes pills from a relative or an old prescription.",
        "Growth checks watch the baby. After birth, sugar is tested again because gestational diabetes raises later diabetes risk. Fever, bleeding, or severe pain in pregnancy needs urgent obstetric care.",
    ),
}


def fmt(text, symptom):
    return text.format(s=symptom) if "{s}" in text else text


def cluster(ids, a, b, tips, urgency="routine", urgent_ids=()):
    ids = list(ids)
    urgent_ids = set(urgent_ids)
    missing = set(ids) - set(tips)
    extra = set(tips) - set(ids)
    if missing or extra:
        raise SystemExit(f"tip mismatch missing={sorted(missing)} extra={sorted(extra)}")
    out = {}
    for i in ids:
        u = "urgent" if i in urgent_ids else urgency
        out[i] = (u, a, b, tips[i])
    return out


def decoy(symptom_id, symptom, condition):
    """Three ways when the row is a poor fit for this condition."""
    library = {
        "fever": (
            "urgent",
            "Fever is not a usual part of {c}. Get a same-day check to find the infection.",
            "Rest and sip fluids while you wait. Do not treat the fever as {c}.",
            "Go to urgent care now if fever comes with severe pain, confusion, vomiting, a spreading rash, or trouble breathing.",
        ),
        "fishy_odor": (
            "soon",
            "A fishy odor is not treated as {c}. It more often means bacterial vaginosis and needs a swab.",
            "Do not douche or use scented washes while you wait. They make the imbalance worse.",
            "After a clinician confirms bacterial vaginosis, metronidazole or clindamycin is the usual antibiotic. Yeast cream does not clear a fishy odor.",
        ),
        "fishy_odor_only": (
            "soon",
            "A fishy odor without pain is not {c}. Ask for a swab for bacterial vaginosis.",
            "Skip douching and scented products until you are examined.",
            "Use the prescribed antibiotic if the swab confirms bacterial vaginosis, and go back if pelvic pain or fever appears.",
        ),
        "burning_urination": (
            "soon",
            "Burning when you urinate is not a {c} treatment target. Get a urine test for a bladder infection.",
            "Drink water and do not start leftover antibiotics.",
            "Same-day care is needed if burning comes with fever, side or back pain, vomiting, pregnancy, or confusion.",
        ),
        "burning_only": (
            "soon",
            "Burning only when you urinate points to a urine infection, not to {c}.",
            "Arrange a urine test and keep drinking water.",
            "Add an urgent visit if fever, back pain, or vomiting starts.",
        ),
        "thick_white_discharge": (
            "soon",
            "Thick white cottage-cheese discharge suggests yeast, not {c}.",
            "A pharmacist or doctor can confirm yeast and choose an azole medicine. In pregnancy, use only a topical product a clinician approves.",
            "Get an exam if this is the first time, if you are pregnant, or if it returns often. Check blood sugar when yeast keeps coming back.",
        ),
        "hot_flashes": (
            "routine",
            "Hot flashes are a menopause symptom, not a feature of {c}. Note your age, cycle changes, and how often the heat comes.",
            "While you wait for a review, dress in layers, keep the bedroom cool, and limit alcohol, caffeine, and spicy food in the evening.",
            "A doctor can separate menopause from a thyroid problem and discuss hormone therapy or nonhormonal options. Do not start hormones on your own.",
        ),
        "breast_lump": (
            "soon",
            "A breast lump is not part of {c}. Book a breast clinic promptly.",
            "Do not wait for the next routine mammogram if the lump is new.",
            "Mammogram and ultrasound decide whether a biopsy is needed. Go sooner if the skin dimples, the nipple pulls in, or there is bloody nipple discharge.",
        ),
        "new_breast_lump": (
            "soon",
            "A new breast lump needs its own breast assessment, not treatment for {c}.",
            "Ask for diagnostic imaging rather than a screening appointment months away.",
            "Watch for skin puckering, nipple change, or bloody discharge and report those at the same visit.",
        ),
        "neck_swelling": (
            "soon",
            "A neck swelling is a thyroid and neck issue, not {c}. Ask for an exam, a TSH blood test, and an ultrasound if a lump is felt.",
            "Do not start high-dose iodine or thyroid hormone on your own.",
            "Urgent care is needed if you have trouble breathing, trouble swallowing, or a rapidly growing painful neck.",
        ),
        "vaginal_itch": (
            "soon",
            "Vaginal itch is not how {c} is treated. An exam separates yeast, bacterial vaginosis, skin irritation, and dryness.",
            "Use plain water, loose cotton underwear, and no scented products until the cause is known.",
            "Match the medicine to the cause: azole for confirmed yeast, an antibiotic for confirmed bacterial vaginosis, or vaginal moisturizer if the cause is dryness.",
        ),
        "irregular_periods": (
            "soon",
            "Irregular periods are not explained by {c}. Take a pregnancy test if pregnancy is possible, then review cycles with a doctor.",
            "Track dates, flow, and skipped months. Common causes include PCOS, thyroid disease, perimenopause, and weight change.",
            "Fewer than eight periods a year needs a plan to protect the uterine lining. Sudden heavy bleeding needs a sooner visit.",
        ),
        "fracture_minor_fall": (
            "urgent",
            "A fracture after a small fall is an osteoporosis pathway, not {c}. Get the bone assessed urgently.",
            "After the break is treated, ask for a bone-density scan and a fall-risk review.",
            "Prescription bone medicine is considered after a low-trauma fracture, along with calcium from food, vitamin D if low, and strength exercise once the bone team allows it.",
        ),
        "green_discharge": (
            "soon",
            "Green discharge is not {c}. It needs a same-week sexual-health swab, including a check for trichomonas and other infections.",
            "Avoid sex until you have been tested, or use condoms if you cannot wait for the visit.",
            "Partners are often treated when trichomonas is found. Fever or deep pelvic pain with discharge needs same-day care.",
        ),
        "frothy_discharge": (
            "soon",
            "Frothy yellow-green discharge suggests trichomonas more than {c}. Get a swab.",
            "Hold off sex or use condoms until the result is back.",
            "Prescribed antibiotics treat trichomonas, and recent partners usually need treatment too.",
        ),
        "green_frothy_discharge": (
            "soon",
            "Green frothy discharge is a reason for an infection swab, not for {c} treatment.",
            "Do not use yeast cream as a substitute for the test.",
            "If the test shows trichomonas, finish the antibiotic and tell recent partners to get treated.",
        ),
        "blisters": (
            "urgent",
            "Blisters or open sores need a same-day sexual-health exam. They are not {c}.",
            "Do not pick the sores or use steroid cream on them before a clinician has seen them.",
            "Herpes treatment works best when started early. Skip sex while sores are open.",
        ),
        "swollen_glands_groin": (
            "soon",
            "Tender groin glands with genital sores or fever need a prompt infection check, not {c} care.",
            "Note any sores, discharge, or pain and tell the clinician.",
            "Go the same day if you also have high fever, rapidly spreading redness, or trouble walking.",
        ),
        "thin_gray_discharge": (
            "soon",
            "Thin gray discharge with odor fits bacterial vaginosis more than {c}.",
            "Ask for a swab and do not douche before the visit.",
            "Metronidazole or clindamycin is used after confirmation. Yeast treatment will not fix gray discharge.",
        ),
        "odor_after_sex": (
            "soon",
            "A strong fishy odor after sex is a bacterial vaginosis clue, not a {c} symptom to treat on its own.",
            "Skip douching. Condoms during treatment are sometimes advised.",
            "Get a swab and use the prescribed antibiotic if bacterial vaginosis is confirmed.",
        ),
        "blood_in_urine": (
            "soon",
            "Blood in the urine needs a urine test. It is not treated as {c}.",
            "Drink water and collect a sample the way the clinic asks. Do not ignore pink, red, or cola-colored urine.",
            "Go the same day if bleeding comes with fever, side pain, clots, fainting, or an inability to pass urine.",
        ),
        "flank_pain": (
            "urgent",
            "Pain in the side under the ribs can be a kidney infection or a kidney stone, not {c}.",
            "Seek same-day care, especially with fever, vomiting, or burning urine.",
            "Do not wait for a routine {c} visit if the pain is severe or you cannot keep fluids down.",
        ),
        "chills": (
            "urgent",
            "Shaking chills mean you should be seen promptly for infection. They are not a {c} treatment target.",
            "Note your temperature and any pain in the pelvis, back, or bladder.",
            "Emergency care is appropriate if chills come with high fever, severe pain, confusion, or vomiting.",
        ),
        "nausea": (
            "soon",
            "Nausea is not a usual part of {c}. Note whether it comes with pain, fever, a missed period, or a new medicine.",
            "Sip fluids and eat small bland portions while you arrange a visit. Do not start antibiotics for nausea alone.",
            "Vomiting that will not stop, severe belly pain, fainting, or possible pregnancy needs same-day care.",
        ),
        "lower_belly_pain": (
            "urgent",
            "Deep lower-belly pain is not treated as {c}. It can be pelvic infection, a cyst complication, or ectopic pregnancy.",
            "Take a pregnancy test if pregnancy is possible, and get an exam today rather than another cream for itch or odor.",
            "Go to emergency care if the pain is severe or if you also have fever, vomiting, fainting, or shoulder-tip pain.",
        ),
        "bleeding_between_periods": (
            "soon",
            "Bleeding between periods is not a {c} treatment target. Take a pregnancy test if pregnancy is possible.",
            "Book a cervical and pelvic check. Do not douche or start hormones on your own to stop the spotting.",
            "Heavy bleeding, dizziness, or pain with the bleeding needs a same-day visit.",
        ),
        "acne": (
            "routine",
            "Acne is not how {c} is managed. A gentle cleanser and a benzoyl peroxide or adapalene product can help mild spots if your skin tolerates them.",
            "See dermatology or a primary doctor if acne is scarring, painful, or adult-onset with irregular periods, which can point to hormones.",
            "Do not use someone else's prescription acne medicine, especially if pregnancy is possible.",
        ),
        "severe_period_pain": (
            "soon",
            "Severe period pain is not a feature to treat as {c}. It needs its own gynecology review for endometriosis and other causes.",
            "A heat pack and an anti-inflammatory, if safe for you, can take the edge off while you book that visit.",
            "Pain that stops daily activity, or pain with fever, fainting, or one-sided sudden severity, needs urgent care.",
        ),
        "bleeding_after_sex": (
            "soon",
            "Bleeding after sex should be checked at a cervical and infection visit. It is not a treatment target of {c}.",
            "Note how much bleeding, whether it is new, and whether there is also pain or discharge.",
            "Do not wait for the next routine Pap if this is a new pattern. Heavy bleeding or pregnancy needs a sooner visit.",
        ),
        "one_sided_pelvic_pain": (
            "urgent",
            "Sudden pain on one side needs urgent care to rule out ovarian torsion, cyst rupture, or ectopic pregnancy. It is not managed as {c}.",
            "Take a pregnancy test if pregnancy is possible, and do not eat or drink if you may need urgent surgery.",
            "Call emergency services if you faint, vomit, or have shoulder-tip pain with the pelvic pain.",
        ),
        "night_sweats_drenching": (
            "soon",
            "Drenching night sweats need a medical review. They are not a {c} treatment by themselves.",
            "Record fever, weight change, cough, and cycle timing to help sort infection, menopause, and other causes.",
            "Same-day care is needed if sweats come with high fever, chest pain, or breathlessness.",
        ),
        "weight_loss": (
            "soon",
            "Weight loss without trying needs a clinician to look for thyroid disease, gut disease, diabetes, infection, and other causes. It is not treated as {c}.",
            "Bring a food recall and a note of how much weight changed over what time.",
            "Add an urgent visit if weight loss comes with black stools, vomiting blood, chest pain, or a new lump.",
        ),
        "leg_swelling": (
            "urgent",
            "New swelling of one leg can be a blood clot. Go to urgent care the same day. It is not a {c} home treatment.",
            "Do not massage the leg hard or start blood thinners on your own.",
            "Emergency care is needed if swelling comes with chest pain, coughing blood, or sudden breathlessness.",
        ),
        "pain_one_side_sudden": (
            "urgent",
            "Sudden one-sided pain that then eases still needs same-day assessment for cyst rupture, torsion, or ectopic pregnancy.",
            "Mention a possible pregnancy and any shoulder pain, fainting, or vomiting.",
            "Do not file this under {c} follow-up if the pain was severe.",
        ),
        "itch_under_breast": (
            "routine",
            "Itch only in the fold under the breast is usually moisture or a skin yeast rash, not {c}.",
            "Keep the fold dry, wear a supportive cotton bra, and ask a pharmacist about an antifungal cream if the skin is red and sore.",
            "See a doctor if the skin breaks, you have fever, or there is a breast lump, dimple, or nipple change.",
        ),
        "heavy_periods": (
            "soon",
            "Heavy periods need their own bleeding assessment. They are not treated by managing {c} alone.",
            "Ask for a blood count and iron test, and an ultrasound if bleeding is new or worsening.",
            "Same-day care is needed if you soak a pad or tampon every hour, faint, or get chest pain.",
        ),
        "vaginal_itch_alone": (
            "soon",
            "Itch alone fits yeast, irritation, or dryness better than {c}.",
            "Stop scented products and get a swab if discharge or soreness is present.",
            "Use the medicine that matches the confirmed cause, and a moisturizer if the clinician finds dryness.",
        ),
    }
    # aliases used in the CSV
    aliases = {
        "vaginal_itch": "vaginal_itch",
    }
    key = aliases.get(symptom_id, symptom_id)
    if key not in library:
        return (
            "soon",
            f"“{symptom}” is an uncommon part of {condition} and should be assessed as its own problem.",
            f"Book a visit to find the cause before you add a medicine aimed at {condition}.",
            "Use only gentle measures such as rest, water, and avoiding irritants until the cause is clear. Seek urgent care for severe pain, heavy bleeding, fainting, fever, chest pain, or trouble breathing.",
        )
    urgency, a, b, c = library[key]
    return (
        urgency,
        a.format(c=condition, s=symptom),
        b.format(c=condition, s=symptom),
        c.format(c=condition, s=symptom),
    )


SPECIFIC = {}

def add(condition, mapping):
    SPECIFIC.setdefault(condition, {}).update(mapping)

# --- PCOS ---
add("PCOS", cluster(
    ["irregular_periods", "cycles_over_35_days", "fewer_than_8_periods", "absent_periods", "heavy_periods", "long_periods"],
    "Track {s} on a calendar and review it with a doctor. Take a pregnancy test if a period is late.",
    "If you are not trying to conceive, a prescribed combined hormonal contraceptive or a progestin brings a planned bleed and protects the uterine lining. If you are trying, letrozole is the usual first step to start ovulation.",
    {
        "irregular_periods": "Bring three to six months of dates. Treatment is aimed at a predictable bleed or at ovulation, depending on whether you want pregnancy.",
        "cycles_over_35_days": "Cycles longer than 35 days still count as too few ovulations. Do not wait a year between check-ins if this pattern is steady.",
        "fewer_than_8_periods": "Fewer than eight periods a year is the point where lining protection becomes important. Ask for that plan explicitly.",
        "absent_periods": "Months without bleeding need a pregnancy test first, then a hormone check. Do not restart a period with leftover pills.",
        "heavy_periods": "When a PCOS period finally comes and is very heavy, ask for a blood count and iron test as well as cycle treatment.",
        "long_periods": "A bleed that lasts many days needs the same lining plan, plus a check that a polyp or fibroid is not adding to the flow.",
    },
    urgency="soon",
))
add("PCOS", cluster(
    ["extra_hair", "extra_facial_hair", "extra_body_hair", "hair_removal_often"],
    "For {s}, hormone treatment slows new growth. A combined contraceptive is first line. Spironolactone is sometimes added if a doctor prescribes it and pregnancy is prevented.",
    "Hair already present is treated with laser, electrolysis, or prescribed eflornithine cream. Waxing and plucking only bridge the gap.",
    {
        "extra_hair": "Expect months, not days, before new hair slows. Photograph an area monthly so you and the doctor can see change.",
        "extra_facial_hair": "Chin and upper-lip hair responds to laser or electrolysis while the hormone medicine reduces regrowth. Avoid plucking if you plan laser.",
        "extra_body_hair": "Chest, abdomen, and thigh hair uses the same hormone plan. Choose a removal method your skin tolerates.",
        "hair_removal_often": "Needing frequent removal means the hormone dose or medicine may need a review, not only a closer shave.",
    },
))
add("PCOS", cluster(
    ["acne", "adult_acne", "oily_skin"],
    "For {s}, use a gentle cleanser and a benzoyl peroxide or adapalene product if your skin tolerates it. Do not scrub.",
    "A prescribed combined contraceptive or spironolactone treats the hormone driver. See dermatology if spots scar.",
    {
        "acne": "Give a skin product six to eight weeks before judging it. Stop and get advice if you are pregnant or trying.",
        "adult_acne": "Acne that continues into adulthood with irregular cycles is a reason to treat the hormones, not only the spots.",
        "oily_skin": "Oil control with a mild cleanser helps comfort. Hormone treatment is what changes the driver.",
    },
))
add("PCOS", cluster(
    ["trouble_conceiving"],
    "For {s}, ask for an ovulation check rather than waiting without a plan. Letrozole is the usual first medicine in PCOS.",
    "A full fertility visit also checks semen and whether the tubes are open. Weight and glucose care improve the chance of ovulation.",
    {"trouble_conceiving": "If ovulation medicine does not lead to pregnancy in the time your clinic sets, move to a fertility specialist instead of repeating unmonitored cycles."},
    urgency="soon",
))
add("PCOS", cluster(
    ["weight_gain", "abdominal_weight"],
    "For {s}, aim for regular walking plus strength work and meals built around protein, vegetables, and slower carbohydrates. Crash diets tend to rebound.",
    "Ask about metformin and about screening for diabetes, cholesterol, and blood pressure. Medicine supports the habit change; it does not replace it.",
    {
        "weight_gain": "Track waist and how clothes fit, not only the scale. Small sustained changes matter more than a short strict plan.",
        "abdominal_weight": "Belly-predominant gain is a metabolic signal in PCOS. Pair activity with a glucose check.",
    },
))
add("PCOS", cluster(
    ["scalp_hair_thinning", "temple_hair_loss"],
    "For {s}, treat the androgen excess and ask for iron and thyroid tests so another cause is not missed.",
    "Topical minoxidil is often added. A combined contraceptive or spironolactone, if safe for you, addresses the hormone side.",
    {
        "scalp_hair_thinning": "Shedding takes months to slow. Use a part-line photo every month rather than judging daily shed.",
        "temple_hair_loss": "Temple thinning can also be genetic. A dermatologist can confirm the pattern before you commit to long-term treatment.",
    },
))
add("PCOS", cluster(
    ["dark_skin_patches", "dark_skin_groin", "skin_tags"],
    "For {s}, the useful treatment is better insulin sensitivity through activity, food pattern, and sometimes metformin. Fading creams do not fix the driver.",
    "Ask for a glucose check. A doctor can confirm acanthosis nigricans, which is the darkened velvety skin linked with insulin resistance.",
    {
        "dark_skin_patches": "Neck and underarm darkening lightens slowly if glucose improves. A dermatologist helps only after that plan is in place.",
        "dark_skin_groin": "Keep folds dry to prevent a second rash. Do not bleach groin skin.",
        "skin_tags": "A clinician can remove a tag that snags or bleeds. New tags are another reason to check sugar.",
    },
))
add("PCOS", cluster(
    ["fatigue", "bloating", "pelvic_pain", "mood_low", "anxiety", "sleep_trouble", "sugar_craving", "increased_hunger", "extra_thirst", "headache", "dandruff", "breast_tenderness", "hot_flashes"],
    "Tell a doctor about {s} and whether it tracks your cycle. It can sit beside PCOS, but it also has other causes worth naming.",
    "Sleep, regular meals, and treatment of the cycle or insulin resistance often help. Add a targeted test if the symptom is strong on its own.",
    {
        "fatigue": "Ask for a blood count, ferritin, thyroid, and glucose. Do not assume tiredness is only PCOS.",
        "bloating": "Note foods and cycle days. Constant bloating with weight loss or a growing belly needs a sooner exam.",
        "pelvic_pain": "PCOS is not mainly a pain disease. Ongoing pelvic pain needs a check for endometriosis, cysts, or infection.",
        "mood_low": "Say clearly if mood is low most days. Counseling and, when needed, mental-health treatment sit alongside hormone care.",
        "anxiety": "Cut caffeine late in the day and ask whether sleep apnea or thyroid disease is adding to the anxiety.",
        "sleep_trouble": "Loud snoring with daytime sleepiness needs a sleep-apnea check, which is more common in PCOS. Side sleeping and a review of bedtime habits help while you wait.",
        "sugar_craving": "Pair carbohydrates with protein and do not skip meals. A glucose test shows whether cravings reflect insulin resistance.",
        "increased_hunger": "Hunger that is new and strong, with thirst and frequent urine, needs a diabetes check soon.",
        "extra_thirst": "Extra thirst is a reason for a glucose test soon, not only a PCOS lifestyle talk.",
        "headache": "Track timing, lights, and any neurologic change. Sudden worst-ever headache or headache with weakness needs urgent care.",
        "dandruff": "An antifungal shampoo used as directed treats scalp dandruff. It does not treat PCOS itself.",
        "breast_tenderness": "Cyclical tenderness often settles when cycles are regulated. A new lump, skin dimple, or nipple discharge needs a breast clinic.",
        "hot_flashes": "Hot flashes raise perimenopause or thyroid disease as the better explanation. Do not start menopause hormones without a review.",
    },
))
for _sid in ("extra_thirst", "increased_hunger", "sleep_trouble"):
    _u, _a, _b, _c = SPECIFIC["PCOS"][_sid]
    SPECIFIC["PCOS"][_sid] = ("soon", _a, _b, _c)
add("PCOS", cluster(
    ["family_pcos", "family_diabetes", "high_blood_pressure"],
    "Use {s} as a reason to screen earlier, not as a symptom to medicate by itself.",
    "Ask for blood pressure, glucose, and cholesterol checks, and keep a home pressure log if a reading was high.",
    {
        "family_pcos": "A mother or sister with PCOS raises your chance. Tracking cycles and androgens is the useful response.",
        "family_diabetes": "A close relative with type 2 diabetes means you should have glucose checked even if you feel well.",
        "high_blood_pressure": "Confirm the reading, limit salt and alcohol, move most days, and take a prescribed pressure medicine if lifestyle steps are not enough. Recheck; do not ignore a single high visit.",
    },
    urgency="soon",
))

# --- Endometriosis ---
add("Endometriosis", cluster(
    ["severe_period_pain", "pain_not_relieved", "pain_before_period", "pain_between_periods", "chronic_pelvic_pain", "pain_worse_over_years", "pain_since_teens", "missed_work", "pain_after_medicine_wears_off", "lower_belly_pain", "lower_back_pain", "leg_pain_period", "pelvic_heaviness", "one_sided_pelvic_pain", "pain_with_exercise"],
    "For {s}, start a heat pack and an anti-inflammatory such as ibuprofen or naproxen if they are safe for you. Begin a day before the period if the pain is predictable.",
    "Ask about continuous hormonal suppression so you have fewer periods. A hormone IUD, progestin, or combined pill used continuously is typical. Do not keep increasing pain-tablet doses on your own.",
    {
        "severe_period_pain": "Pain that stops daily activity deserves a gynecology referral, a pain diary, and a talk about laparoscopy if hormones fail.",
        "pain_not_relieved": "If ordinary tablets do nothing, that is a reason to change the plan, not to stack extra doses.",
        "pain_before_period": "Starting the anti-inflammatory just before pain usually begins works better than waiting for the peak.",
        "pain_between_periods": "Pain on non-period days needs a specialist plan. Infection and ovarian cysts should be ruled out.",
        "chronic_pelvic_pain": "Pelvic-floor physical therapy and a pain clinic add benefit when pain is present most days.",
        "pain_worse_over_years": "Worsening over years is a reason to revisit diagnosis and to image or refer, not to normalize it.",
        "pain_since_teens": "Long-standing pain from the first periods still deserves treatment. Young people can use hormonal suppression under a clinician.",
        "missed_work": "Bring a simple count of days lost. It supports referral and a stronger hormone or surgical plan.",
        "pain_after_medicine_wears_off": "Pain that returns when a dose wears off may need a scheduled anti-inflammatory plus hormones, not only as-needed tablets.",
        "lower_belly_pain": "Constant lower-belly pain with fever, vomiting, or pregnancy risk needs same-day care to exclude infection, torsion, or ectopic pregnancy.",
        "lower_back_pain": "Cyclical back pain can be endometriosis. Constant back pain with leg weakness or bladder loss needs urgent care.",
        "leg_pain_period": "Pain into the thigh with the period should be written into the diary. It can change how surgery is planned.",
        "pelvic_heaviness": "A heavy pelvis also needs an ultrasound so a cyst or fibroid is not missed.",
        "one_sided_pelvic_pain": "Mainly one-sided pain needs an ultrasound. Sudden severe increase, fainting, or vomiting is an emergency.",
        "pain_with_exercise": "Modify workouts around the period and keep moving in ways that do not spike pain. Do not stop all activity long term without a rehab plan.",
    },
    urgency="soon",
    urgent_ids=("lower_belly_pain",),
))
add("Endometriosis", cluster(
    ["pain_with_sex", "pain_after_sex"],
    "For {s}, pause deep penetration when it hurts, try positions you control, and use a lubricant. Pain with sex is a core endometriosis symptom and belongs in the specialist visit.",
    "Hormonal suppression and, when needed, surgical treatment of deep disease reduce this pain. Pelvic-floor therapy helps muscle guarding that stays after the disease is treated.",
    {
        "pain_with_sex": "Say whether pain is at entry or deep. Deep pain points more toward endometriosis or the cervix and changes the exam.",
        "pain_after_sex": "Aching afterward should be timed in the diary. Bleeding after sex needs a cervical check as well.",
    },
    urgency="soon",
))
add("Endometriosis", cluster(
    ["painful_bowel_on_period", "rectal_pain_period", "diarrhea_on_period", "constipation_on_period", "blood_in_stool_period"],
    "For {s}, record that it happens with the period. Bowel endometriosis is treated by a gynecologist, sometimes with a bowel surgeon.",
    "Hormone suppression reduces cyclical bowel pain for many people. Fiber, fluids, and a gentle laxative if a clinician agrees help constipation days. Do not assume it is only irritable bowel if it is strictly cyclical.",
    {
        "painful_bowel_on_period": "Mention painful bowel movements at the endometriosis visit so imaging and surgical consent include the bowel.",
        "rectal_pain_period": "Rectal pain with periods is a reason for a specialist, not only a hemorrhoid cream.",
        "diarrhea_on_period": "Cyclical diarrhea can ease when periods are suppressed. Sudden diarrhea with fever is a different, infectious problem.",
        "constipation_on_period": "Fluids, fiber, and movement help the constipated days while hormone treatment addresses the cycle.",
        "blood_in_stool_period": "Blood in the stool needs a doctor even if it only appears with the period. Large amounts, black stools, or dizziness need urgent care.",
    },
    urgency="soon",
))
add("Endometriosis", cluster(
    ["pain_urinating_on_period", "pain_full_bladder"],
    "For {s}, tell the gynecologist the bladder hurts with the cycle. A urine test should still rule out infection.",
    "Hormone suppression is the medical treatment. Bladder endometriosis sometimes needs a specialist surgeon.",
    {
        "pain_urinating_on_period": "Pain only during the period is different from a bladder infection. Get a urine test once so infection is not missed.",
        "pain_full_bladder": "Note pain as the bladder fills. Drinking little to avoid pain can cause other problems; treat the cause instead.",
    },
    urgency="soon",
))
add("Endometriosis", cluster(
    ["nausea", "vomiting", "bloating", "fatigue", "heavy_periods", "spotting_before_period", "bleeding_between_periods", "trouble_conceiving", "shoulder_pain_period", "family_endometriosis", "mood_low", "dizziness"],
    "Include {s} in the pain and cycle diary you take to endometriosis care.",
    "Treating the cycle with hormones, iron if bleeding has made you anemic, and a fertility plan when you need one covers most of these linked problems.",
    {
        "nausea": "An anti-nausea plan from your clinician, small meals, and better pain control usually help period nausea.",
        "vomiting": "Vomiting with period pain means pain control is failing. Seek care if you cannot keep fluids down.",
        "bloating": "Cyclical bloating often tracks the period. Bloating that is constant or comes with weight loss needs a separate exam.",
        "fatigue": "Check iron and ferritin if periods are heavy. Pace activity and treat night pain that breaks sleep.",
        "heavy_periods": "Heavy flow is treated with tranexamic acid or hormones if safe for you, plus an iron test.",
        "spotting_before_period": "Spotting before a period should be logged. Pregnancy, infection, and a polyp still need to be considered.",
        "bleeding_between_periods": "Bleeding between periods needs a pregnancy test and a cervical check, not only an endometriosis label.",
        "trouble_conceiving": "Ask for a fertility discussion early. Laparoscopy is sometimes part of care when pain and infertility travel together. Do not wait years in silence.",
        "shoulder_pain_period": "Cyclical shoulder-tip pain can be diaphragmatic endometriosis and should be told to the surgeon. Shoulder pain with collapse or possible pregnancy is an emergency.",
        "family_endometriosis": "A mother or sister with endometriosis raises your chance. The useful step is a symptom diary and an earlier referral, not a medicine taken because of family history alone.",
        "mood_low": "Ongoing pain and low mood should both be treated. Ask for mental-health support at the same time as gynecology care.",
        "dizziness": "Dizziness with heavy flow needs a blood count. Fainting needs same-day care.",
    },
    urgency="soon",
))

# --- Uterine fibroids ---
add("Uterine Fibroids", cluster(
    ["heavy_periods", "long_periods", "large_clots", "soaking_hourly", "flooding_at_night", "bleeding_between_periods"],
    "For {s}, ask a doctor about tranexamic acid or an anti-inflammatory on bleeding days, if they are safe for you, and about a hormone IUD or other hormonal option.",
    "A blood count and iron test look for anemia. Ultrasound confirms fibroid size and location, which decides whether medicine, embolization, or surgery fits.",
    {
        "heavy_periods": "Count how many pads or tampons you use. That number helps the doctor choose medicine versus a procedure.",
        "long_periods": "Bleeding more than seven days is a reason to treat, not to buy more pads and wait.",
        "large_clots": "Clots larger than a coin should be described at the visit. They often travel with iron deficiency.",
        "soaking_hourly": "Soaking a pad or tampon within an hour is heavy enough for same-day care if it continues for several hours, especially with dizziness.",
        "flooding_at_night": "Flooding at night is treated with the same bleeding plan. A towel and overnight protection are coping steps, not the treatment.",
        "bleeding_between_periods": "Bleeding between periods still needs a pregnancy test and a check of the uterine lining, even when fibroids are known.",
    },
    urgency="soon",
    urgent_ids=("soaking_hourly",),
))
add("Uterine Fibroids", cluster(
    ["pelvic_pressure", "fullness", "lower_abdomen_swelling", "frequent_urination", "night_urination", "trouble_emptying_bladder", "constipation", "bulk_with_bending", "clothes_tighter", "pain_on_one_side"],
    "For {s}, medicine that shrinks fibroids for a time, or a procedure that removes or blocks their blood supply, is what relieves bulk. Pain tablets do not shrink a fibroid.",
    "Ultrasound or MRI shows which fibroid is pressing. Myomectomy keeps the uterus if you want pregnancy. Embolization and hysterectomy are other options a specialist explains.",
    {
        "pelvic_pressure": "Pressure that limits walking or bending is a reason to discuss a procedure, not only another pain tablet.",
        "fullness": "Fullness low in the belly should be imaged so ovarian enlargement is not mistaken for a fibroid.",
        "lower_abdomen_swelling": "A firm lower-belly swelling needs an exam. Do not wrap or bind it.",
        "frequent_urination": "A urine test rules out infection. If the test is clear, fibroid pressure is treated by shrinking or removing the fibroid.",
        "night_urination": "Cut evening caffeine and get a urine test. Night waking from pressure improves when bulk is treated.",
        "trouble_emptying_bladder": "Trouble emptying is a reason for a sooner visit. Sudden inability to pass urine is an emergency.",
        "constipation": "Fluids, fiber, and movement help, but rectal pressure from a fibroid needs the fibroid treated if stool symptoms are new and strong.",
        "bulk_with_bending": "Pressure when you bend is a bulk symptom to quote at the surgical consult.",
        "clothes_tighter": "Clothes tighter only at the lower belly should be matched to an ultrasound, not to a weight-loss plan alone.",
        "pain_on_one_side": "A dull one-sided ache needs ultrasound. A sudden sharp twist in the pain needs urgent care for degeneration or torsion.",
    },
    urgency="soon",
))
add("Uterine Fibroids", cluster(
    ["lower_back_pain", "leg_pain", "bloating", "pain_with_sex", "period_pain", "sudden_sharp_pain", "nausea", "headache"],
    "For {s}, use heat and an anti-inflammatory if safe for you while a clinician confirms the fibroid is the cause.",
    "Lasting pain, pain with sex, or a sudden severe change needs ultrasound and a treatment talk. Sudden sharp pain with vomiting or fainting needs the emergency department.",
    {
        "lower_back_pain": "Back pain from fibroids is treated by treating the fibroid. New weakness, numbness, or bladder loss needs urgent care.",
        "leg_pain": "Aching into the legs should be mentioned. New one-sided calf swelling needs a clot check.",
        "bloating": "Bloating that is actually a firm swelling should be examined rather than treated as gas.",
        "pain_with_sex": "Pain with sex from a low fibroid may improve with position changes short term and with removal or shrinkage as the real treatment.",
        "period_pain": "Worse cramps are helped by anti-inflammatories and by lightening the period. A new severe pattern still needs imaging.",
        "sudden_sharp_pain": "Sudden sharp pelvic pain needs same-day care to rule out fibroid degeneration, torsion of a pedunculated fibroid, or another emergency.",
        "nausea": "Nausea with pressure often eases when pain and bulk are treated. Vomiting with severe pain is urgent.",
        "headache": "Headache with heavy bleeding can be anemia. Check a blood count. A sudden severe headache needs urgent care.",
    },
    urgency="soon",
    urgent_ids=("sudden_sharp_pain",),
))
add("Uterine Fibroids", cluster(
    ["fatigue", "dizziness", "pale_skin", "shortness_of_breath", "fast_heartbeat", "ice_craving", "trouble_conceiving"],
    "For {s}, ask for a blood count and ferritin the same week. Heavy fibroid bleeding commonly causes iron deficiency.",
    "Replace iron as prescribed and treat the bleeding so the iron loss stops. Chest pain, fainting, or breathlessness at rest needs urgent care.",
    {
        "fatigue": "Tiredness that limits the day often improves after iron and lighter periods. Do not only drink more caffeine.",
        "dizziness": "Sit or lie down if you spin. Repeated dizziness with heavy flow is a reason for a same-week blood count, and fainting is same-day care.",
        "pale_skin": "Pale skin with heavy periods is a classic anemia sign. Confirm with a blood test and start iron only as directed.",
        "shortness_of_breath": "Breathlessness on stairs from anemia improves when iron and bleeding are treated. Breathlessness at rest or with chest pain is urgent.",
        "fast_heartbeat": "A racing heart with little effort needs a blood count. Chest pain or fainting with it is an emergency.",
        "ice_craving": "Craving ice is a strong clue to low iron. Tell the doctor and get ferritin checked.",
        "trouble_conceiving": "Fibroids that distort the uterine cavity can affect pregnancy. A fertility-aware surgeon should decide whether removal helps. Do not start embolization if you want a near-term pregnancy without that talk.",
    },
    urgency="soon",
))

# --- Heavy periods ---
add("Heavy Periods", cluster(
    ["soaking_hourly", "soaking_several_hours", "double_protection", "flooding_at_night", "up_at_night_to_change", "long_periods", "large_clots", "many_clots", "cycles_under_21_days", "bleeding_limits_day", "clothes_or_sheets", "bleeding_between_periods", "bleeding_after_sex", "cramps", "pelvic_pressure", "lower_back_pain"],
    "For {s}, a clinician can use tranexamic acid or an anti-inflammatory during the bleed, if safe for you, and a hormone IUD, pill, or progestin for the cycles ahead.",
    "Ultrasound looks for fibroids and polyps. A bleeding diary that counts pad changes is the most useful thing to bring.",
    {
        "soaking_hourly": "Soaking protection every hour for several hours needs same-day care, especially with dizziness.",
        "soaking_several_hours": "Changing every hour across several hours is the definition of bleeding that should not be watched at home.",
        "double_protection": "Needing a pad and a tampon together is enough to start medical treatment. You do not have to faint first.",
        "flooding_at_night": "Night flooding is treated with the bleeding plan. Set an alarm only as a safety step while you wait for care.",
        "up_at_night_to_change": "Getting up more than once to change is a diary fact that supports starting treatment now.",
        "long_periods": "Periods longer than seven days need a cause and a medicine plan, not only more supplies.",
        "large_clots": "Describe clots larger than a coin. They belong in the visit and often mean you need an iron test.",
        "many_clots": "Many clots in one day should be written down with the pad count.",
        "cycles_under_21_days": "Periods closer than 21 days raise total blood loss. A pregnancy test and a cycle plan are the next steps.",
        "bleeding_limits_day": "Bleeding that keeps you home is a reason for treatment and, if you feel faint, for same-day care.",
        "clothes_or_sheets": "Soaking clothes or sheets shows the volume is high. Bring that description; do not minimize it.",
        "bleeding_between_periods": "Bleeding between periods needs a pregnancy test and a cervical check as well as a bleeding plan.",
        "bleeding_after_sex": "Bleeding after sex needs a cervical and infection check. Do not wait for a routine screen.",
        "cramps": "Cramps with heavy flow often ease when an anti-inflammatory is started early and the flow is lightened.",
        "pelvic_pressure": "Pressure plus heavy bleeding raises the chance of fibroids. Ask for an ultrasound.",
        "lower_back_pain": "Back pain with the period can follow heavy cramps. Treat the bleed and seek care if weakness or bladder changes appear.",
    },
    urgency="soon",
    urgent_ids=("soaking_hourly", "soaking_several_hours"),
))
add("Heavy Periods", cluster(
    ["fatigue", "weakness", "dizziness", "fainting", "pale_skin", "pale_nails", "shortness_of_breath", "fast_heartbeat", "chest_tightness", "headache", "ice_craving", "cold_hands", "trouble_concentrating", "irritability", "nausea"],
    "For {s}, get a blood count and ferritin. Replacing iron and slowing the bleeding are the two treatments that work together.",
    "Take iron as prescribed, away from tea, coffee, and thyroid medicine. Keep tablets away from children. Fainting, chest pain, or gasping breath needs urgent care.",
    {
        "fatigue": "Tiredness during the period often tracks anemia. Rest helps the day; iron and lighter periods fix the cause.",
        "weakness": "Weakness on heavy days is a reason to be seen this week, sooner if you cannot stand safely.",
        "dizziness": "Sit down when dizzy. Repeated dizziness with bleeding needs a blood count this week.",
        "fainting": "Fainting with a period is same-day care. Do not drive yourself if you still feel near fainting.",
        "pale_skin": "Pale skin should be confirmed with a blood test before you start high-dose iron on your own.",
        "pale_nails": "Pale nail beds support an anemia check. They recover after iron stores return, which takes weeks.",
        "shortness_of_breath": "Breathlessness on stairs needs a blood count soon. Breathlessness at rest is urgent.",
        "fast_heartbeat": "A pounding heart with heavy bleeding needs a blood count. Chest pain with it is an emergency.",
        "chest_tightness": "Chest tightness with a heavy period needs urgent care to rule out severe anemia and heart strain.",
        "headache": "Period headaches can follow blood loss and dehydration. A sudden severe headache needs urgent care.",
        "ice_craving": "Craving ice is a clue to iron deficiency. Mention it; doctors use it as a real symptom.",
        "cold_hands": "Cold hands with pallor fit anemia. Warming them is comfort; iron and bleeding control are the treatment.",
        "trouble_concentrating": "Fog during heavy days often improves when anemia is corrected and sleep is restored.",
        "irritability": "Irritability on the heaviest days is worth naming. It often tracks pain, poor sleep, and anemia.",
        "nausea": "Nausea with cramps eases when pain is treated. Inability to keep fluids down needs a sooner visit.",
    },
    urgency="soon",
    urgent_ids=("fainting", "chest_tightness"),
))
add("Heavy Periods", cluster(
    ["one_sided_pelvic_pain"],
    "Sudden pain on one side is not ordinary heavy-period cramp. Get same-day care for torsion, rupture, or ectopic pregnancy.",
    "Take a pregnancy test if pregnancy is possible. Do not eat or drink if surgery may be needed.",
    {"one_sided_pelvic_pain": "Call emergency services if the pain comes with fainting, vomiting, or shoulder-tip pain."},
    urgency="urgent",
))

# --- UTI ---
add("Urinary Tract Infection", cluster(
    ["burning_urination", "pain_end_of_stream", "urgency", "frequent_urination", "small_amounts", "night_urination", "cloudy_urine", "strong_urine_smell", "blood_in_urine", "lower_belly_pain", "bladder_pressure", "incomplete_emptying", "hesitancy", "new_leaking", "symptoms_over_hours", "pain_walking", "back_pain_low"],
    "For {s}, get a urine test and start the antibiotic a clinician prescribes. Finish the course even when burning fades.",
    "Drink water through the day. Phenazopyridine can numb the bladder for a short time if a pharmacist agrees. It is not an antibiotic and it turns urine orange.",
    {
        "burning_urination": "Burning that is new over hours is the classic reason to be tested today, not next week.",
        "pain_end_of_stream": "Pain at the end of the stream still needs a urine test. Do not wait for blood to appear.",
        "urgency": "Urgency improves after antibiotics start. Go sooner if you also have fever or side pain.",
        "frequent_urination": "Going often with only drops suggests cystitis. A test confirms it before you take random pills.",
        "small_amounts": "Passing small amounts is part of bladder irritation. Antibiotics plus fluids are the treatment, not fluid restriction.",
        "night_urination": "Many night trips with burning deserve a test. Cutting evening caffeine helps comfort only.",
        "cloudy_urine": "Cloudy urine supports getting a sample. It does not prove infection by itself.",
        "strong_urine_smell": "A new strong smell with burning should be tested. Smell alone, without other symptoms, is not a reason to take antibiotics.",
        "blood_in_urine": "Pink or cola urine with urinary pain needs a test promptly. Heavy bleeding or clots need same-day care.",
        "lower_belly_pain": "Pain just above the pubic bone fits cystitis. Spreading pain with fever needs a kidney check.",
        "bladder_pressure": "Constant pressure is treated by clearing the infection. A heating pad is only comfort.",
        "incomplete_emptying": "A feeling of not emptying should be rechecked after antibiotics. Lasting retention needs a clinician, and inability to pass any urine is urgent.",
        "hesitancy": "Trouble starting the stream still gets a urine test. In older adults, review constipation and medicines too.",
        "new_leaking": "New leaking with infection often settles after treatment. Lasting leaking needs a separate continence plan.",
        "symptoms_over_hours": "Symptoms that worsen over a day should not be watched over a weekend if fever or vomiting appears.",
        "pain_walking": "Discomfort when walking usually eases as the infection clears. Fever changes this to urgent care.",
        "back_pain_low": "Low backache with urinary symptoms needs a clinician to decide bladder versus kidney. Side pain under the ribs with fever is urgent.",
    },
    urgency="soon",
))
add("Urinary Tract Infection", cluster(
    ["fever", "chills", "flank_pain", "nausea", "vomiting", "feeling_unwell", "confusion"],
    "For {s} together with urinary symptoms, seek same-day care. This pattern can be a kidney infection and needs antibiotics chosen for that, sometimes in hospital.",
    "Do not rely on a pharmacy urinary pain reliever alone. Sip fluids if you can keep them down.",
    {
        "fever": "Fever plus burning urine is not a simple cystitis to wait out.",
        "chills": "Shaking chills with urinary pain belong in urgent care.",
        "flank_pain": "Pain under the ribs on one side is a kidney warning. Go the same day.",
        "nausea": "Nausea with urinary pain needs assessment. Inability to drink is a reason for urgent care.",
        "vomiting": "Vomiting means oral antibiotics may not stay down. Seek care rather than retrying tablets at home.",
        "feeling_unwell": "Feeling much more ill than a usual bladder irritation, especially with fever, needs same-day review.",
        "confusion": "New confusion in an older adult can be the main sign of urine or kidney infection. Arrange same-day care and do not leave them alone if they are unsafe.",
    },
    urgency="urgent",
))
add("Urinary Tract Infection", cluster(
    ["pelvic_pain_both_sides"],
    "Pelvic pain on both sides with discharge may be pelvic inflammatory disease rather than a simple urine infection.",
    "Get an exam the same day. A urine test alone can miss it.",
    {"pelvic_pain_both_sides": "Fever, deep pain with sex, or vomiting with this pain means emergency or same-day gynecology care."},
    urgency="urgent",
))

# --- Yeast ---
add("Yeast Infection", cluster(
    ["thick_white_discharge", "increased_white_discharge", "vaginal_itch", "itch_worse_at_night", "vulvar_burning", "vaginal_soreness", "redness", "swelling", "raw_skin", "satellite_rash", "little_odor", "pain_with_sex", "pain_after_sex", "burning_urination", "external_burn_only", "worse_before_period", "after_antibiotics", "recurrent_itch", "worse_when_warm", "discomfort_sitting", "white_patches", "pain_wiping"],
    "For {s}, use an azole cream or suppository for the full labeled course, or a single fluconazole tablet if a pharmacist or doctor says it fits you. In pregnancy, do not take oral fluconazole; get a topical plan from a clinician.",
    "Keep the area dry, wear loose cotton underwear, and skip scented pads and washes. A cool compress can calm the skin while medicine works.",
    {
        "thick_white_discharge": "Cottage-cheese discharge with itch is the usual yeast picture. If there is a strong fishy smell instead, you need a bacterial vaginosis test, not another yeast course.",
        "increased_white_discharge": "More white discharge without itch may be normal. Treat as yeast only if itch, burning, or a clinician agrees.",
        "vaginal_itch": "Strong itch is the symptom azole medicine targets. If it is the first episode, an exam is safer than guessing.",
        "itch_worse_at_night": "Night itch eases as the azole course works. Trim nails so you do not break the skin.",
        "vulvar_burning": "Apply external cream to the sore skin as the product allows, and avoid soap on the area.",
        "vaginal_soreness": "Soreness should improve over the course. Worsening pain or fever means stop self-treatment and be examined.",
        "redness": "Redness of the vulva fits yeast. Marked one-sided swelling or fever needs a visit.",
        "swelling": "Swelling of the labia can follow yeast. Get a same-day exam if swelling is severe, one-sided, or you cannot pass urine.",
        "raw_skin": "Raw cracks need the azole plus a plain barrier if a pharmacist agrees. Steroid cream only if a clinician adds it.",
        "satellite_rash": "A rash onto the groin can be a skin yeast infection. Dry the folds and ask about an antifungal cream for the skin as well as vaginal treatment.",
        "little_odor": "Little odor supports yeast over bacterial vaginosis. A strong fishy odor should change the treatment.",
        "pain_with_sex": "Wait to have sex until soreness settles. Lubricant helps afterward; it does not replace the antifungal.",
        "pain_after_sex": "Soreness after sex should fade as the infection clears. Bleeding after sex needs a cervical check.",
        "burning_urination": "Burning when urine touches sore skin is external. A urine test is still wise if you also have urgency or fever.",
        "external_burn_only": "External burning is treated with external azole cream. Internal tablets alone may miss the skin.",
        "worse_before_period": "Flares before a period can still be treated with a standard course. If every cycle flares, ask about a longer plan.",
        "after_antibiotics": "Yeast after antibiotics is common. Finish the antibiotic unless a doctor tells you to stop, and treat the yeast.",
        "recurrent_itch": "Four or more episodes a year need a confirmed swab, a longer antifungal plan, and a glucose check. Do not live on repeated single-dose tablets without that.",
        "worse_when_warm": "Heat and tight clothes worsen itch. Change out of wet workout clothes promptly while the medicine works.",
        "discomfort_sitting": "A cool compress and loose clothes help sitting pain during the treatment days.",
        "white_patches": "White patches should be seen if they do not clear with one course. Lichen sclerosus and other skin diseases can mimic yeast.",
        "pain_wiping": "Pat dry instead of rubbing. Pain that prevents toileting needs an exam.",
    },
    urgency="soon",
))
add("Yeast Infection", {
    "increased_white_discharge": (
        "routine",
        "More white discharge than usual, without itch or burning, is often normal. Do not start an antifungal only because discharge increased.",
        "Get a swab if the discharge is new, smells strongly, or comes with itch, pain, or bleeding.",
        "If yeast is confirmed, finish an azole course. In pregnancy, use a topical product a clinician chooses rather than oral fluconazole.",
    ),
})

# --- BV ---
add("Bacterial Vaginosis", cluster(
    ["fishy_odor", "odor_after_sex", "odor_after_period", "thin_gray_discharge", "more_discharge", "watery_discharge", "discharge_in_underwear", "little_itch", "mild_irritation", "mild_burning", "after_period", "symptoms_come_and_go", "odor_noticed_by_partner", "worse_during_period", "burning_urination", "pelvic_pain", "pain_with_sex", "vaginal_itch", "redness"],
    "For {s}, get a swab if you can. Confirmed bacterial vaginosis is treated with prescribed metronidazole or clindamycin, by mouth or in the vagina.",
    "Do not douche. Follow the alcohol advice on metronidazole. Yeast cream will not remove a fishy odor.",
    {
        "fishy_odor": "A fishy odor is the symptom that should trigger a test, not a perfumed wash.",
        "odor_after_sex": "Semen can make the odor stronger. Condoms during treatment are sometimes advised. The antibiotic is still the treatment.",
        "odor_after_period": "Blood raises vaginal pH and can unmask odor. Treat after confirmation rather than after every period automatically.",
        "thin_gray_discharge": "Thin gray or milky discharge plus odor is the usual picture. Thick white itch-dominant discharge is more often yeast.",
        "more_discharge": "A larger amount of thin discharge is treated with the antibiotic once the swab fits. Do not use internal cleanses.",
        "watery_discharge": "Watery discharge that is new still deserves a look so infection and, if relevant, other causes are not missed.",
        "discharge_in_underwear": "A thin film in underwear matches this pattern. Bring the description; you do not need a photo.",
        "little_itch": "Little or no itch actually fits bacterial vaginosis better than yeast. Do not buy an antifungal for odor alone.",
        "mild_irritation": "Mild irritation settles as the antibiotic works. Severe pain or fever is a different illness.",
        "mild_burning": "Mild burning can come from discharge on the skin. A urine test is wise if burning is mainly when you pass urine.",
        "after_period": "Symptoms after a period are a reason to be treated if the swab confirms bacterial vaginosis, not a reason to douche.",
        "symptoms_come_and_go": "Symptoms that return need a longer or suppressive plan from a clinician, not a new home remedy each month.",
        "odor_noticed_by_partner": "A partner noticing odor is a fair reason to be tested. Ask whether that partner needs any care for your specific result.",
        "worse_during_period": "A flare with bleeding still uses the same antibiotic after confirmation. Avoid treating only with menstrual products.",
        "burning_urination": "Add a urine test. Bacterial vaginosis treatment does not cure a bladder infection.",
        "pelvic_pain": "Pelvic pain is not typical of uncomplicated bacterial vaginosis. Get an exam for pelvic inflammatory disease if pain is deep or you have fever.",
        "pain_with_sex": "Pain with sex plus odor needs an exam, not only an antibiotic called in without a look.",
        "vaginal_itch": "Strong itch is less typical. Ask the clinician to check for yeast at the same time.",
        "redness": "Marked redness and swelling need an exam so yeast or skin infection is not missed.",
    },
    urgency="soon",
))

# --- PID ---
add("Pelvic Inflammatory Disease", cluster(
    ["lower_belly_pain", "pain_constant", "pain_worse_days", "severe_pain_fever", "fever", "chills", "feeling_unwell", "pain_with_sex", "pain_after_sex", "unusual_discharge", "yellow_discharge", "discharge_with_odor", "bleeding_between_periods", "bleeding_after_sex", "heavier_period", "lower_back_pain", "pain_walking", "pain_on_exam_movement", "burning_urination", "frequent_urination", "nausea", "vomiting", "right_upper_belly_pain", "fatigue", "lost_appetite", "irregular_bleeding", "pain_both_sides"],
    "For {s}, go to a clinic or emergency department the same day. Pelvic inflammatory disease is treated with combination antibiotics after an exam.",
    "Finish every dose even when pain starts to ease. Rest, skip sex until a clinician says you may resume, and make sure recent partners are treated.",
    {
        "lower_belly_pain": "Pain on both sides of the lower belly with discharge or fever should not be watched overnight.",
        "pain_constant": "Pain present most of the day is beyond ordinary period cramp. Be examined today.",
        "pain_worse_days": "Pain that has built over a few days still needs same-day antibiotics once the diagnosis is made. Do not start leftover pills.",
        "severe_pain_fever": "Severe pain plus fever belongs in the emergency department. Hospital treatment is sometimes required.",
        "fever": "Fever with pelvic pain is a danger sign. Go now rather than taking only a fever reducer.",
        "chills": "Shaking chills with pelvic pain need emergency assessment.",
        "feeling_unwell": "Feeling much sicker than with a normal period is a reason for emergency or same-day gynecology care.",
        "pain_with_sex": "Deep pain with sex plus discharge can be this infection. Stop sex and get examined.",
        "pain_after_sex": "Pain that continues after sex should be included in the same-day visit.",
        "unusual_discharge": "New unusual discharge with pelvic pain needs testing for sexually transmitted infections and a full antibiotic plan.",
        "yellow_discharge": "Yellow or green discharge is part of the picture to test, not to deodorize.",
        "discharge_with_odor": "Odor plus pain is more than bacterial vaginosis. You need an exam today.",
        "bleeding_between_periods": "Unexpected bleeding with pain needs a pregnancy test and an infection exam.",
        "bleeding_after_sex": "Bleeding after sex is reported at the same visit. Do not wait for a routine Pap.",
        "heavier_period": "A heavier period with new pain and fever is not a reason to stay home with a hot water bottle.",
        "lower_back_pain": "Back pain with fever and pelvic pain belongs in the same urgent assessment.",
        "pain_walking": "Pain when you walk is a severity marker. Get care today.",
        "pain_on_exam_movement": "Pain when the lower belly is pressed is a finding a clinician uses. Do not repeatedly prod the belly hard at home.",
        "burning_urination": "A urine test is done too, because a bladder infection can travel with this illness. It does not replace the pelvic exam.",
        "frequent_urination": "Needing to urinate more often is noted, then the pelvic infection is still fully treated.",
        "nausea": "Nausea with pelvic pain and fever needs same-day care. Sip fluids only if you are not heading straight to emergency surgery assessment.",
        "vomiting": "Vomiting means you may not keep antibiotic tablets down. Go to emergency care.",
        "right_upper_belly_pain": "New pain under the right ribs with pelvic pain can mean the infection has tracked upward. This is emergency care.",
        "fatigue": "Fatigue follows the infection. The treatment is still prompt antibiotics and rest, plus follow-up.",
        "lost_appetite": "Lost appetite with pelvic pain should not delay the visit. Drink if you can while you travel to care.",
        "irregular_bleeding": "Bleeding at unexpected times needs a pregnancy test as part of the same-day exam.",
        "pain_both_sides": "Pain on both sides supports this diagnosis over a single ovarian cyst, but you still need an exam today to be sure.",
    },
    urgency="urgent",
))

# --- Menopause ---
add("Menopause", cluster(
    ["hot_flashes", "hot_flash_daytime", "night_sweats", "waking_hot", "palpitations"],
    "For {s}, menopausal hormone therapy is the most effective treatment when a doctor finds it safe for you.",
    "If hormones are not used, ask about certain antidepressants, gabapentin, fezolinetant, cognitive behavioral therapy, a cool bedroom, layers, and less alcohol and caffeine.",
    {
        "hot_flashes": "Track how many flashes you have in a day. That number helps choose whether lifestyle steps are enough or a medicine should start.",
        "hot_flash_daytime": "A small fan, layers you can remove, and avoiding a hot trigger before a meeting are practical while medicine is decided.",
        "night_sweats": "A cool room, moisture-wicking sleepwear, and a light duvet help the night. Soaking sweats that ruin sleep deserve a treatment talk.",
        "waking_hot": "Waking overheated is treated the same way as night sweats. Keep water by the bed; do not add a heavy blanket back immediately.",
        "palpitations": "A flutter during a hot flash is common, but a doctor should hear about it. Chest pain, fainting, or a sustained racing heart needs urgent care.",
    },
    urgency="routine",
))
add("Menopause", cluster(
    ["period_change_midlife", "skipped_periods", "periods_stopped_12_months", "lighter_then_stop", "heavier_in_transition", "cycle_length_change", "bleeding_after_menopause"],
    "For {s}, a clinician should confirm where you are in the menopause transition and rule out pregnancy, thyroid disease, and problems in the uterus if bleeding is heavy or unexpected.",
    "Hormone therapy or a progestin plan can steady troublesome bleeding in perimenopause. After 12 months with no period, any bleeding is investigated before hormones are used to stop it.",
    {
        "period_change_midlife": "Spacing or stopping of periods in midlife is expected. Keep a calendar so a sudden change in the pattern is obvious.",
        "skipped_periods": "Skipped months need a pregnancy test if pregnancy is possible. Contraception is still needed until a clinician confirms it is no longer required.",
        "periods_stopped_12_months": "Twelve months without a period is menopause. Contraception advice and bone and heart health are the next conversations.",
        "lighter_then_stop": "Lighter periods that stop can be watched if you feel well. Hot flashes and sleep can still be treated.",
        "heavier_in_transition": "Heavier periods before they stop are common but not something to endure. Ask about a hormone IUD, tranexamic acid, and an ultrasound.",
        "cycle_length_change": "Cycles that jump shorter or longer should be logged. Very frequent bleeding needs a sooner visit.",
        "bleeding_after_menopause": "Any bleeding after a year without periods needs a prompt gynecology visit, ultrasound, and often sampling. Do not start hormones to hide it.",
    },
    urgency="soon",
    urgent_ids=(),
))
# bleeding after menopause is soon/prompt, override by replacing urgency
SPECIFIC["Menopause"]["bleeding_after_menopause"] = (
    "soon",
    SPECIFIC["Menopause"]["bleeding_after_menopause"][1],
    SPECIFIC["Menopause"]["bleeding_after_menopause"][2],
    SPECIFIC["Menopause"]["bleeding_after_menopause"][3],
)

add("Menopause", cluster(
    ["vaginal_dryness", "pain_with_sex", "burning_vaginal", "itch_from_dryness", "lower_interest_sex", "bladder_urgency", "recurrent_urine_burn"],
    "For {s}, start a vaginal moisturizer used regularly and a lubricant during sex. These are not the same product.",
    "Low-dose vaginal estrogen, prescribed after a clinician checks that it fits you, is the most effective treatment for genitourinary syndrome of menopause. It is different from full-body hormone therapy.",
    {
        "vaginal_dryness": "Use moisturizer several times a week, not only when you plan sex. Improvement takes a few weeks.",
        "pain_with_sex": "Pain from dryness should not be pushed through. Lubricant, moisturizer, and vaginal estrogen treat it. Pelvic-floor therapy helps if muscles have tightened.",
        "burning_vaginal": "Burning from dryness is treated with moisturizers and vaginal estrogen. A swab is wise the first time so infection is not missed.",
        "itch_from_dryness": "Mild itch without thick discharge fits dryness. Thick white discharge needs a yeast check before you add steroid cream.",
        "lower_interest_sex": "Interest often returns when pain and sleep improve. Relationship counseling and, when appropriate, a hormone discussion are further options.",
        "bladder_urgency": "Urgency can improve with vaginal estrogen and bladder training. A urine test rules out infection first.",
        "recurrent_urine_burn": "Burning that keeps returning needs urine cultures. Vaginal estrogen lowers recurrent urine infections for many postmenopausal people. Do not take leftover antibiotics.",
    },
))
add("Menopause", cluster(
    ["sleep_trouble", "insomnia", "mood_low", "irritability", "anxiety", "joint_aches", "muscle_aches", "fatigue", "weight_gain", "scalp_hair_thinning", "dry_skin", "chin_hair", "brain_fog", "headache", "dry_eyes", "breast_tenderness", "dizzy_spells"],
    "For {s}, treat night sweats and sleep first, because they drive mood, fog, and fatigue. Hormone therapy or a nonhormonal flash treatment is the medical lever.",
    "Keep a wind-down hour, limit alcohol, and move most days. Ask a clinician to check thyroid, iron, and blood pressure when the symptom does not fit a simple flash pattern.",
    {
        "sleep_trouble": "A cool room and treating flashes help more than a leftover sleep tablet. Ask before using any sleep medicine.",
        "insomnia": "If you wake and cannot return to sleep, get out of bed for a short calm break rather than watching the clock. Cognitive behavioral therapy for insomnia is an effective treatment.",
        "mood_low": "Low mood that lasts most days needs mental-health care as well as menopause care. Say so directly at the visit.",
        "irritability": "Irritability often tracks poor sleep. Treating sweats and protecting sleep is the first medical step.",
        "anxiety": "New anxiety in midlife can be menopause-related and still deserves its own support, including therapy and, when needed, medicine.",
        "joint_aches": "Regular strength and mobility work helps aches. A clinician should see a hot swollen joint, which is not a menopause symptom.",
        "muscle_aches": "Muscle aches ease with sleep, activity, and vitamin D if you are low. Sudden severe muscle pain with dark urine needs urgent care.",
        "fatigue": "Fatigue needs a check for anemia, thyroid disease, and sleep apnea if you snore, alongside menopause treatment.",
        "weight_gain": "Midlife weight around the middle responds to strength training and a steady eating pattern. Hormones are not a weight-loss drug.",
        "scalp_hair_thinning": "Thinning on the scalp is assessed for iron, thyroid, and pattern hair loss. Minoxidil is often used. Do not start high-dose hormones for hair alone.",
        "dry_skin": "A plain thick moisturizer and shorter hot showers help dry skin. This does not replace vaginal treatment if the main dryness is genital.",
        "chin_hair": "A few coarse chin hairs can be removed by plucking or electrolysis. Sudden heavy hair growth needs a hormone check.",
        "brain_fog": "Word-finding trouble often improves when sleep and flashes are treated. Report confusion that is sudden or worsening quickly.",
        "headache": "Headaches that change with the cycle should be logged. A new severe headache or neurologic symptom is urgent.",
        "dry_eyes": "Artificial tears and a screen break help dry eyes. An eye clinician should see pain, light sensitivity, or vision change.",
        "breast_tenderness": "Tenderness while periods are changing often settles. A new lump or skin change needs a breast clinic.",
        "dizzy_spells": "Brief dizziness should be checked, including blood pressure and anemia. Fainting, chest pain, or one-sided weakness is an emergency.",
    },
))

# --- Osteoporosis ---
add("Osteoporosis", cluster(
    ["fracture_minor_fall", "fracture_from_cough", "hip_or_wrist_break", "spine_break_little_trauma", "prior_fracture_after_50", "sudden_back_pain", "back_pain_bending", "pain_lasting_weeks", "pain_when_coughing"],
    "For {s}, get the bone assessed urgently or promptly depending on pain and whether a break is obvious. Do not walk on a suspected hip fracture.",
    "After the acute break is treated, a bone-density scan and a fracture-risk review lead to a prescribed bone medicine for most people with a low-trauma fracture.",
    {
        "fracture_minor_fall": "A break after a small fall is a low-trauma fracture. Urgent bone care comes first; osteoporosis treatment follows so the next bone does not break.",
        "fracture_from_cough": "A rib or spine fracture after a cough is not normal aging. Get imaging and a bone plan.",
        "hip_or_wrist_break": "A hip or wrist break from standing height needs emergency orthopedic care. Later, ask for osteoporosis treatment before you leave follow-up.",
        "spine_break_little_trauma": "A spine fracture with little injury needs pain control, a check that the spinal cord is safe, and then bone medicine.",
        "prior_fracture_after_50": "Another fracture after 50 means treatment should already be in place. If it is not, book the bone clinic now.",
        "sudden_back_pain": "Sudden mid or upper back pain can be a spine fracture. Get imaging rather than weeks of unexplained pain.",
        "back_pain_bending": "Pain when you bend may be a wedge fracture. A clinician should examine you before you start aggressive stretching.",
        "pain_lasting_weeks": "Back pain for weeks after a minor strain needs a look for a fracture, especially if you are past menopause or on steroids.",
        "pain_when_coughing": "Sharp back pain when you cough can be a broken vertebra. Support the spine and get assessed. Sudden leg weakness or loss of bladder control is an emergency.",
    },
    urgency="soon",
    urgent_ids=("fracture_minor_fall", "hip_or_wrist_break", "spine_break_little_trauma", "fracture_from_cough"),
))
add("Osteoporosis", cluster(
    ["height_loss", "height_loss_inches", "stooped_posture", "hump_upper_back", "clothes_waist", "shorter_than_remembered", "difficulty_standing_straight", "less_height_each_year", "abdomen_protrudes", "short_of_breath_curve", "no_daily_pain"],
    "For {s}, ask for a spine assessment and a bone-density scan. Height loss and a new curve can be silent spine fractures.",
    "Bone medicine, posture and back-strength exercise taught by a physio, and fall prevention are the treatment. Do not force the spine straight with aggressive manipulation.",
    {
        "height_loss": "Compare with a young-adult height. Loss of about an inch or more deserves imaging.",
        "height_loss_inches": "Losing more than about an inch is a fracture clue, not just aging posture.",
        "stooped_posture": "A new stoop should be imaged. Exercise helps remaining strength; it does not shove a fracture back into place.",
        "hump_upper_back": "A new upper-back hump needs a spine X-ray and a bone plan.",
        "clothes_waist": "A changing waistline with height loss can mean the spine is compressing. Mention both facts together.",
        "shorter_than_remembered": "If friends notice you look shorter, measure and tell your doctor. Silent fractures are common.",
        "difficulty_standing_straight": "Difficulty standing straight needs a physio plan that avoids flexion strain, plus bone treatment.",
        "less_height_each_year": "Height that drops every year should trigger a scan, not another note that you are shorter.",
        "abdomen_protrudes": "A belly that sticks out as the spine curves is a mechanical result of vertebral collapse. Core bracing comes from a physio, and the bone still needs medicine.",
        "short_of_breath_curve": "Breathlessness from a rounding spine should be assessed so heart and lung causes are not missed. Breathing exercises help mechanics after that check.",
        "no_daily_pain": "Osteoporosis often has no daily pain until a fracture. The treatment is the scan and prevention, not waiting to hurt.",
    },
))
add("Osteoporosis", cluster(
    ["family_fracture", "early_menopause", "periods_stopped_young", "steroid_use", "low_body_weight", "tooth_loss", "fatigue", "joint_aches", "muscle_weakness"],
    "Use {s} as a reason to measure bone density and fall risk sooner.",
    "Calcium from food, vitamin D if low, strength and balance training, stopping smoking, and limiting alcohol are the base. Prescription bone medicine is added when risk is high.",
    {
        "family_fracture": "A parent with a hip fracture raises your risk. Book a density scan rather than waiting for your own fracture.",
        "early_menopause": "Menopause before 45 needs a bone plan. Hormone therapy is sometimes the right protection; a clinician decides.",
        "periods_stopped_young": "Periods that stopped young need a cause and a bone-protection plan, including a look at estrogen.",
        "steroid_use": "Long use of steroid tablets is a major bone risk. Ask for a bone-protection medicine while steroids continue. Do not stop steroids suddenly.",
        "low_body_weight": "Very low weight raises fracture risk. Nutrition support matters alongside the bone scan.",
        "tooth_loss": "Early tooth loss is a prompt to check bone density. Tell your dentist if you start a bone medicine, because some medicines affect dental procedures.",
        "fatigue": "Fatigue is not treated with bone drugs. Look for anemia, thyroid disease, and poor sleep, and still do the bone checks your risk requires.",
        "joint_aches": "General joint aches need movement and a check for arthritis. A hot swollen joint is not osteoporosis.",
        "muscle_weakness": "A weak grip or trouble rising from a chair is treated with strength and balance training and a check for vitamin D deficiency. This also lowers fall risk.",
    },
))

# --- Ovarian cysts ---
add("Ovarian Cysts", cluster(
    ["one_sided_pelvic_pain", "dull_one_sided_ache", "sudden_sharp_pain", "pain_mid_cycle", "period_pain", "pain_after_exercise", "pain_with_sex", "pain_after_sex", "pain_to_thigh", "nausea_with_pain", "vomiting_with_pain", "dizzy_with_sudden_pain", "shoulder_tip_pain", "pain_that_settles", "pain_before_period", "lower_back_pain"],
    "For {s}, get an ultrasound and a pregnancy test if pregnancy is possible. Many simple cysts are watched because they resolve.",
    "Heat and an anti-inflammatory, if safe for you, can ease a mild ache. Sudden severe pain, fainting, vomiting, or shoulder-tip pain needs the emergency department for torsion, rupture, or ectopic pregnancy.",
    {
        "one_sided_pelvic_pain": "One-sided pain should not be blamed on a period until imaging says so.",
        "dull_one_sided_ache": "A dull ache that comes and goes can be watched if ultrasound shows a simple cyst and you are well. Agree the follow-up date.",
        "sudden_sharp_pain": "Sudden sharp pain is same-day or emergency care, especially with vomiting or near-fainting.",
        "pain_mid_cycle": "A brief mid-cycle twinge can be ovulation. Pain that is severe or does not settle still needs assessment.",
        "period_pain": "Pain that only flares with a period may be endometriosis or a cyst. A diary plus ultrasound sorts the next step.",
        "pain_after_exercise": "Pain after exercise that settles can be watched after a clinician has seen the ultrasound. Pain that worsens needs urgent review.",
        "pain_with_sex": "One-sided pain during sex should be in the ultrasound request. Stop the activity that reproduces severe pain.",
        "pain_after_sex": "Aching after sex is logged and imaged. Bleeding after sex also needs a cervical check.",
        "pain_to_thigh": "Pain into the thigh is still consistent with a cyst. New leg swelling needs a clot check.",
        "nausea_with_pain": "Nausea with sudden pelvic pain is a reason for emergency care, not for a home anti-nausea tablet alone.",
        "vomiting_with_pain": "Vomiting with sudden severe pain needs the emergency department.",
        "dizzy_with_sudden_pain": "Feeling faint with sudden pain can mean internal bleeding. This is an emergency.",
        "shoulder_tip_pain": "Shoulder-tip pain with severe pelvic pain can mean irritation from blood in the abdomen. Go to emergency care.",
        "pain_that_settles": "Pain that is severe and then eases still needs a timely ultrasound and pregnancy test. Do not ignore it because it faded.",
        "pain_before_period": "Pain the week before a period should be in the diary. A simple cyst may be observed; a complex cyst is not.",
        "lower_back_pain": "Low back ache on the same side is included in the pain map. Bowel or urinary red flags are assessed too.",
    },
    urgency="soon",
    urgent_ids=("sudden_sharp_pain", "vomiting_with_pain", "dizzy_with_sudden_pain", "shoulder_tip_pain"),
))
add("Ovarian Cysts", cluster(
    ["bloating", "fullness", "lower_abdomen_swelling", "pressure", "frequent_urination", "trouble_emptying_bladder", "constipation", "irregular_periods", "heavy_periods", "bleeding_between_periods", "fever", "pain_both_sides_constant", "weight_gain_months", "trouble_conceiving"],
    "For {s}, an ultrasound is the test that shows whether a cyst explains it. A pregnancy test is added when bleeding or pain is new.",
    "Simple cysts are often rechecked. A cyst that is large, complex, or still there on the follow-up scan is managed by a gynecologist. Constant bloating for weeks also deserves a timely exam.",
    {
        "bloating": "Bloating that comes and goes with a known simple cyst can be watched. Bloating most days for several weeks needs a clinician, not only a cyst label.",
        "fullness": "Fullness low in the belly is imaged. Do not start a laxative as the only response.",
        "lower_abdomen_swelling": "A swelling felt on one side should be examined. Do not press it repeatedly.",
        "pressure": "Pelvic pressure from a cyst improves if the cyst resolves or is removed. Agree which of those applies to your scan.",
        "frequent_urination": "Rule out a urine infection. If the urine is clear, pressure from the cyst is treated by treating the cyst.",
        "trouble_emptying_bladder": "A feeling of not emptying needs a clinician. Inability to pass urine is urgent.",
        "constipation": "Fluids and fiber help new constipation. A cyst plan is still required if imaging shows pressure on the bowel.",
        "irregular_periods": "Irregular periods are not caused by most simple cysts. Look for pregnancy, PCOS, or thyroid disease as well.",
        "heavy_periods": "Heavy periods need a bleeding and iron plan. A cyst is not automatically the cause.",
        "bleeding_between_periods": "Spotting between periods needs a pregnancy test and a cervical check along with the ultrasound.",
        "fever": "Fever is not a feature of an ordinary cyst. Fever with pelvic pain needs same-day care for infection or another acute problem.",
        "pain_both_sides_constant": "Constant pain on both sides for many days may be infection or endometriosis rather than one cyst. Get examined.",
        "weight_gain_months": "Steady weight gain over months is not how a simple cyst presents. Review diet, thyroid, and other causes, and still report a growing belly.",
        "trouble_conceiving": "Most cysts do not cause infertility. Ask for a fertility workup if you have been trying, rather than treating the cyst as the whole explanation.",
    },
    urgency="soon",
    urgent_ids=("fever",),
))

# --- Cervical screening ---
add("Cervical Screening", cluster(
    ["bleeding_after_sex", "bleeding_after_menopause", "bleeding_between_periods", "spotting_after_screening_not", "watery_bloody_discharge", "bloody_discharge", "unusual_discharge", "discharge_bad_odor", "heavier_periods", "longer_periods", "pelvic_pain", "pain_with_sex", "lower_back_pain", "pain_when_urinating", "bleeding_after_exam"],
    "For {s}, book a cervical and pelvic assessment promptly. These symptoms are investigated; they are not a reason to wait for the next routine screening letter.",
    "The visit may include an exam, infection tests, HPV testing, and ultrasound. Treatment depends on the finding, from infection care to referral for cell changes.",
    {
        "bleeding_after_sex": "Bleeding after sex is a classic reason for a prompt cervical look. Do not wait a year for a routine Pap.",
        "bleeding_after_menopause": "Any bleeding after menopause needs urgent-timed gynecology care, with ultrasound and often sampling.",
        "bleeding_between_periods": "Bleeding between periods needs a pregnancy test and a cervical check.",
        "spotting_after_screening_not": "New spotting that is not just a day or two after a recent test should be reported. A little spotting right after a swab can be normal and should still be mentioned if it continues.",
        "watery_bloody_discharge": "Watery discharge tinged with blood needs a prompt exam.",
        "bloody_discharge": "Brown or bloody discharge is assessed the same way. Do not mask it with douching.",
        "unusual_discharge": "Unusual discharge is tested for infection and examined. Describe color and smell in plain words.",
        "discharge_bad_odor": "Unpleasant odor with discharge needs a swab. If there is also pain or fever, go the same day.",
        "heavier_periods": "Heavier periods need a bleeding assessment as well as up-to-date screening.",
        "longer_periods": "Periods that last longer than they used to should be logged and checked.",
        "pelvic_pain": "Pelvic pain with abnormal bleeding needs an exam soon, including a pregnancy test if relevant.",
        "pain_with_sex": "Pain with sex is reported with any bleeding. Infection, dryness, and cervical disease are sorted at the visit.",
        "lower_back_pain": "Persistent lower back pain is not diagnosed as cervical disease from home. Get an exam if it sits with bleeding or discharge.",
        "pain_when_urinating": "Add a urine test. Cervical care does not replace treatment of a bladder infection.",
        "bleeding_after_exam": "A small amount of spotting for a short time after an exam can happen. Bleeding that continues or is heavy needs a call back, not weeks of waiting.",
    },
    urgency="soon",
))
add("Cervical Screening", cluster(
    ["screening_due", "screening_letter", "overdue_screen", "prior_abnormal", "hpv_letter", "result_unclear", "no_symptoms"],
    "For {s}, the treatment is to attend the test or the follow-up. Screening works when the appointment happens.",
    "An abnormal HPV or Pap result leads to a repeat test or colposcopy. That visit, not a supplement or a douche, is how cell changes are found and treated early.",
    {
        "screening_due": "Book the Pap or HPV test even though you have no symptoms. Put the date on a calendar you will see.",
        "screening_letter": "The invitation letter is the cue to book, not to file. Take the letter with you.",
        "overdue_screen": "An overdue test should be booked now. Say it is overdue so the clinic prioritizes it.",
        "prior_abnormal": "A past abnormal result means you follow the surveillance interval you were given, which may be sooner than a routine screen.",
        "hpv_letter": "HPV found on a test is common and often clears. Complete the exact next step in the letter. Vaccination is discussed if you are still eligible.",
        "result_unclear": "An unclear result needs a repeat, not a guess. Book the repeat in the time window written on the letter.",
        "no_symptoms": "No symptoms is the best time to screen. Cervical cell changes often cause nothing until later.",
    },
    urgency="routine",
))
add("Cervical Screening", cluster(
    ["fatigue", "night_sweats_drenching", "weight_loss"],
    "For {s}, see a clinician to look for a cause. Do not attribute it to waiting for a Pap result.",
    "Bring a note of fever, cough, bleeding, and how much weight changed.",
    {
        "fatigue": "Fatigue has many causes, including anemia and thyroid disease. Cervical screening still happens, but it is not the treatment for tiredness.",
        "night_sweats_drenching": "Drenching night sweats need a medical review. Add same-day care if you have a high fever or feel seriously ill.",
        "weight_loss": "Weight loss without trying needs a clinician. Mention any bleeding or new pain at that visit.",
    },
    urgency="soon",
))
add("Cervical Screening", cluster(
    ["leg_swelling"],
    "New swelling of one leg can be a blood clot and needs same-day care.",
    "Do not massage the leg or start blood thinners yourself.",
    {"leg_swelling": "Chest pain, coughing blood, or sudden breathlessness with leg swelling is an emergency."},
    urgency="urgent",
))

# --- Breast screening ---
add("Breast Screening", cluster(
    ["new_breast_lump", "lump_that_stays", "lump_hard", "lump_growing", "thickening", "skin_dimpling", "skin_like_orange", "nipple_pulled_in", "nipple_points_differently", "bloody_nipple_discharge", "clear_nipple_discharge", "discharge_one_side", "armpit_lump", "lump_above_collarbone", "shape_change", "one_breast_larger", "skin_thickening", "redness", "warmth", "nipple_crusting", "nipple_sore", "rash_on_nipple", "veins_more_visible", "pain_one_spot"],
    "For {s}, contact a doctor promptly for a breast exam and diagnostic imaging. This is not the same as waiting for a routine screening mammogram.",
    "Ultrasound and mammogram, chosen for your age, decide the next step. Biopsy is added if imaging stays concerning. Do not rely on supplements, creams, or watching for several months.",
    {
        "new_breast_lump": "A new lump is assessed even if it is small and even if a recent screening mammogram was normal.",
        "lump_that_stays": "A lump still there after a period needs imaging. Cyclical lumpiness that fully vanishes is different, and a clinician should still hear about a lump you can clearly feel.",
        "lump_hard": "A hard lump is higher priority. Book promptly and do not squeeze it to test it.",
        "lump_growing": "A lump that is getting larger should be imaged now. Note the date you first felt it.",
        "thickening": "A thickened area is assessed the same way as a round lump.",
        "skin_dimpling": "Dimpling or puckering needs a prompt breast clinic. Photograph it in similar light to show the change.",
        "skin_like_orange": "Skin like an orange peel needs urgent breast assessment. Do not treat it as a skin allergy.",
        "nipple_pulled_in": "A nipple that newly pulls inward is a prompt referral. A nipple that has always been inverted is a different story; a new change is what matters.",
        "nipple_points_differently": "A nipple that has changed direction should be examined with the breast, not ignored as posture.",
        "bloody_nipple_discharge": "Bloody discharge from the nipple needs a breast clinic soon, even if you cannot feel a lump.",
        "clear_nipple_discharge": "Clear discharge from one breast is assessed. Do not squeeze the nipple repeatedly; squeezing can keep discharge going.",
        "discharge_one_side": "Discharge from one nipple only is the pattern that needs assessment. Mention color and whether it is spontaneous.",
        "armpit_lump": "A new armpit lump needs a clinician. Infections can cause tender glands, and a persisting lump still gets imaged.",
        "lump_above_collarbone": "A new lump above the collarbone should be seen promptly.",
        "shape_change": "A change in size or shape is a reason for an exam, especially if it is one breast.",
        "one_breast_larger": "One breast newly larger than the other should be examined. Note whether the skin or nipple also changed.",
        "skin_thickening": "Thickening of the skin is imaged. Do not apply steroid cream as the only step.",
        "redness": "A red area that does not fade needs a prompt visit. If the breast is also hot, swollen, and you have a fever, go the same day for infection care, and still complete cancer assessment if it does not fully settle.",
        "warmth": "A warm patch is examined. Fever with a warm painful breast is same-day care.",
        "nipple_crusting": "Crusting or scaling on one nipple that does not heal with simple moisturizer needs a breast clinic. Do not pick it off repeatedly.",
        "nipple_sore": "A nipple sore that does not heal in a short time needs assessment. Keep it clean and dry until seen.",
        "rash_on_nipple": "A rash on one nipple only should be seen if it persists. A rash in both folds under the breasts is more often moisture.",
        "veins_more_visible": "Newly prominent veins on one breast are worth an exam, especially with swelling or a lump.",
        "pain_one_spot": "Pain in one spot that does not go away should be examined. Most breast pain is not cancer, and a focal persistent spot is still checked.",
    },
    urgency="soon",
))
add("Breast Screening", cluster(
    ["breast_pain", "screening_due", "screening_letter", "prior_callback", "family_breast_cancer", "milky_discharge_both", "pain_both_cyclical"],
    "For {s}, follow the screening or clinical path that matches it. Routine screening is for people without a new warning sign.",
    "Bring prior images to callbacks. A family history of breast cancer is a reason to ask whether your screening should start earlier or include extra imaging.",
    {
        "breast_pain": "Breast pain without a lump is often cyclical or musculoskeletal. A well-fitted bra, a pain diary, and a clinician visit if it persists are the steps. Imaging is added when the exam or history warrants it.",
        "screening_due": "Book the mammogram when it is due even if you feel well.",
        "screening_letter": "Use the invitation letter to book. Take it to the appointment.",
        "prior_callback": "A past callback means you should keep future appointments and bring the earlier report. Most callbacks are not cancer.",
        "family_breast_cancer": "A mother, sister, or daughter with breast cancer should be discussed so your start age and test type are personalized. Know their age at diagnosis if you can.",
        "milky_discharge_both": "Milky discharge from both breasts can relate to hormones or medicine. A clinician should review medicines and prolactin. Do not keep squeezing.",
        "pain_both_cyclical": "Pain in both breasts before a period often settles after the period. A supportive bra and an anti-inflammatory, if safe for you, help. A new lump is a separate, prompt visit.",
    },
    urgency="routine",
))
add("Breast Screening", cluster(
    ["fever"],
    "Fever with a red painful breast needs same-day care for mastitis or an abscess, especially in breastfeeding. Treatment is clinical assessment, and often antibiotics or drainage.",
    "Keep feeding or expressing if you are breastfeeding, unless a clinician tells you to stop. Cool compresses are comfort only.",
    {"fever": "If redness and swelling do not improve quickly on the antibiotic, go back. Inflammatory breast cancer is uncommon but is why a non-settling red breast is rechecked."},
    urgency="urgent",
))

# --- Thyroid ---
add("Thyroid Disorder", cluster(
    ["neck_swelling", "neck_swelling_swallow", "tightness_in_neck", "trouble_swallowing", "hoarse_voice", "heat_in_neck"],
    "For {s}, ask for a neck exam, a TSH blood test, and an ultrasound if a lump is present. Some lumps need a needle biopsy.",
    "Do not start iodine supplements or thyroid hormone to shrink a lump. Treatment depends on whether the gland is overactive, underactive, or structurally abnormal.",
    {
        "neck_swelling": "A swelling at the front of the neck should be seen soon. Note how fast it appeared.",
        "neck_swelling_swallow": "A swelling that moves when you swallow is typical of the thyroid. That fact helps the ultrasound request.",
        "tightness_in_neck": "A tight feeling needs an exam. Sudden tightness with breathing trouble is emergency care.",
        "trouble_swallowing": "Trouble swallowing is a prompt visit. Inability to swallow fluids is urgent.",
        "hoarse_voice": "A hoarse voice lasting more than a few weeks needs a look at the throat and thyroid, not only lozenges.",
        "heat_in_neck": "A sense of heat over the neck is reported with the blood tests. It does not tell you to take iodine.",
    },
    urgency="soon",
))
add("Thyroid Disorder", cluster(
    ["weight_change", "weight_gain", "weight_loss", "cold_intolerance", "heat_intolerance", "fatigue", "feeling_slowed", "slow_heartbeat", "fast_heartbeat", "palpitations", "tremor", "sweating", "scalp_hair_thinning", "hair_shedding", "dry_skin", "warm_moist_skin", "puffy_face", "constipation", "loose_stools", "increased_appetite", "mood_low", "anxiety", "irritability", "sleep_trouble", "brain_fog", "muscle_cramps", "muscle_weakness", "brittle_nails", "eye_bulging", "eye_grittiness", "swollen_legs", "cold_hands"],
    "For {s}, a TSH test is the first step. Underactive thyroid is treated with levothyroxine taken as prescribed, usually on an empty stomach, away from iron and calcium. Overactive thyroid is treated with antithyroid medicine, radioactive iodine, or surgery, and sometimes a beta blocker for a racing heart.",
    "Doses are adjusted by repeat blood tests, not by how you feel on a single day. Do not use someone else's thyroid pills or a high-dose iodine product.",
    {
        "weight_change": "Weight change that does not match eating is a reason for TSH, not for a crash diet or unprescribed hormone.",
        "weight_gain": "Weight gain with coldness, slow thinking, and constipation fits underactive thyroid. Levothyroxine, once the dose is right, treats the hormone deficit. It is not a weight-loss pill for people with a normal thyroid.",
        "weight_loss": "Weight loss with heat, tremor, and a fast heart fits overactive thyroid and needs prompt blood tests. Eating more does not treat it.",
        "cold_intolerance": "Feeling unusually cold is reported with the TSH. Dressing warmly is comfort while the dose is set.",
        "heat_intolerance": "Feeling unusually hot with a fast heart should be tested soon. Do not add extra thyroid hormone.",
        "fatigue": "Fatigue from underactive thyroid improves over weeks of the correct levothyroxine dose. Check iron and sleep if fatigue remains.",
        "feeling_slowed": "Feeling slowed in body and mind is a classic underactive symptom. Do not drive if you are too drowsy to be safe, and start treatment through a clinician.",
        "slow_heartbeat": "A heartbeat that feels slow should be checked, including TSH and sometimes an ECG. Fainting with a slow heart is urgent.",
        "fast_heartbeat": "A fast heart with heat and tremor needs prompt thyroid tests. Chest pain or fainting is an emergency.",
        "palpitations": "Palpitations are often eased with a beta blocker while an overactive thyroid is treated. Get urgent care if they come with chest pain or collapse.",
        "tremor": "Shaky hands from an overactive thyroid settle as the hormone level is controlled. Cut excess caffeine in the meantime.",
        "sweating": "New heavy sweating is included in the overactive-thyroid story. Infection with fever is a separate same-day problem.",
        "scalp_hair_thinning": "Thinning hair can follow either thyroid extreme. It recovers slowly after hormone levels are normal. Ask for iron studies too.",
        "hair_shedding": "Extra hair in the shower should be mentioned. Shedding lags behind the blood tests by months.",
        "dry_skin": "Dry skin from underactive thyroid needs the hormone treated plus a plain moisturizer. Thyroid pills bought online are unsafe.",
        "warm_moist_skin": "Warm moist skin fits overactive thyroid and supports getting TSH tested soon.",
        "puffy_face": "A puffy face with other slow symptoms fits underactive thyroid. Sudden swelling of the tongue or lips is an allergic emergency, not thyroid puffiness.",
        "constipation": "Constipation improves as underactive thyroid is corrected. Fluids, fiber, and movement help meanwhile. Do not rely on daily stimulant laxatives without advice.",
        "loose_stools": "More frequent loose stools with weight loss fit overactive thyroid. Blood or black stools need urgent care.",
        "increased_appetite": "Increased appetite with weight loss is a hormone pattern to test, not a reason to start a diet pill.",
        "mood_low": "Low mood can be part of thyroid disease and still needs mental-health care if it is severe or you feel unsafe.",
        "anxiety": "Anxiety or feeling on edge can be the overactive thyroid itself. Treating the thyroid is the medical step; say if anxiety is overwhelming.",
        "irritability": "Irritability often eases when an overactive thyroid is controlled. Protect sleep while tests are pending.",
        "sleep_trouble": "Trouble sleeping with heat and a fast heart should be tested. Do not use someone else's sleep or thyroid medicine.",
        "brain_fog": "Trouble concentrating from thyroid disease improves after levels normalize. Report confusion that is sudden.",
        "muscle_cramps": "Cramps and aches are noted and often improve with treatment. Severe weakness or dark urine needs urgent care.",
        "muscle_weakness": "Weakness climbing stairs can be thyroid-related muscle change. Get the blood test and avoid sudden extreme exercise until you are assessed.",
        "brittle_nails": "Brittle nails recover slowly. Thyroid treatment is the driver; nail cosmetics are optional.",
        "eye_bulging": "Eyes that look more prominent can be thyroid eye disease. Ask for an eye specialist as well as thyroid treatment. Sudden vision loss or double vision is urgent. Do not smoke; smoking worsens thyroid eye disease.",
        "eye_grittiness": "Gritty watery eyes can be early thyroid eye disease. Lubricating drops help the surface. An eye exam is needed if prominence, pain, or vision change appears.",
        "swollen_legs": "Swelling of the lower legs needs an exam so heart, kidney, and thyroid causes are sorted. One leg only, especially with pain, needs a same-day clot check.",
        "cold_hands": "Cold hands with other slow symptoms fit the underactive picture. Warming them is comfort; the blood test guides treatment.",
    },
    urgency="soon",
))
add("Thyroid Disorder", cluster(
    ["irregular_periods", "heavier_periods", "lighter_periods", "family_thyroid"],
    "For {s}, include a TSH test in the period or family-risk visit. Correcting thyroid hormone often steadies cycles.",
    "A pregnancy test comes first if a period is late. Family history is a reason to test sooner, not a reason to take thyroid hormone preventively.",
    {
        "irregular_periods": "Irregular periods can be thyroid, PCOS, or pregnancy. Test before you start a hormone contraceptive as the only step if symptoms of thyroid disease are also present.",
        "heavier_periods": "Heavier periods from underactive thyroid need a blood count and iron test as well as levothyroxine if the TSH confirms it.",
        "lighter_periods": "Lighter or fewer periods can fit overactive thyroid. Confirm with blood tests rather than assuming menopause if other thyroid signs are present.",
        "family_thyroid": "A close relative with thyroid disease is a reason to have TSH checked if you have symptoms, and to tell your doctor the family history at screening.",
    },
    urgency="soon",
))

# --- Iron-deficiency anemia ---
add("Iron-Deficiency Anemia", cluster(
    ["fatigue", "exhaustion_after_little", "pale_skin", "pale_eyelids", "pale_nails", "pale_gums", "dizziness", "fainting", "shortness_of_breath", "breathless_talking", "fast_heartbeat", "pounding_in_ears", "headache", "reduced_exercise", "trouble_concentrating", "irritability", "low_mood", "poor_appetite", "cold_hands"],
    "For {s}, confirm iron deficiency with a blood count and ferritin, then take iron the way it is prescribed. Intravenous iron is used if tablets fail, are not tolerated, or anemia is severe.",
    "Find the blood loss. Heavy periods, pregnancy, low intake, and gut bleeding are the usual places to look. Treating only with iron while bleeding continues does not hold.",
    {
        "fatigue": "Tiredness that limits the day often lifts over a few weeks of iron. Recheck the blood count rather than stopping early because you feel a little better.",
        "exhaustion_after_little": "Exhaustion after light activity is a severity marker. Ask for the blood result and whether intravenous iron is more appropriate.",
        "pale_skin": "Pale skin is confirmed with the blood test. Do not start several iron products at once.",
        "pale_eyelids": "Pale inner eyelids are a useful sign to mention. The lab test still decides the dose.",
        "pale_nails": "Pale nail beds recover after stores recover. That takes longer than the first energy improvement.",
        "pale_gums": "Pale gums should be distinguished from gum disease. Mention both the color and any bleeding gums.",
        "dizziness": "Dizziness on standing needs a blood count soon. Stand up slowly meanwhile. Fainting is same-day care.",
        "fainting": "Feeling faint, or actually fainting, with signs of anemia needs same-day care.",
        "shortness_of_breath": "Breathlessness on mild effort needs a prompt blood count. Breathlessness at rest is urgent.",
        "breathless_talking": "Feeling breathless while talking is significant. Seek care promptly, and urgently if it is worsening.",
        "fast_heartbeat": "A fast heartbeat with little effort can be anemia. Chest pain with it is an emergency.",
        "pounding_in_ears": "A whooshing sound in the ears can come with anemia and should be in the history. It is another reason to check the blood count, not to start ear drops.",
        "headache": "Headaches may ease as anemia corrects. A sudden explosive headache needs urgent care.",
        "reduced_exercise": "Being unable to keep your usual walking pace should improve as hemoglobin rises. Return to exercise gradually.",
        "trouble_concentrating": "Trouble concentrating often tracks fatigue and low hemoglobin. Correcting iron is the treatment, plus sleep.",
        "irritability": "Irritability with exhaustion is worth naming. It is not a character flaw and it often eases as anemia improves.",
        "low_mood": "Low mood with tiredness may need mental-health support as well as iron, especially if it persists after the blood count recovers.",
        "poor_appetite": "A poor appetite makes oral iron harder. Ask about taking it with a small vitamin C-rich food, or about intravenous iron if you cannot eat enough.",
        "cold_hands": "Cold hands and feet improve as anemia improves. Warming them is comfort only.",
    },
    urgency="soon",
    urgent_ids=("fainting",),
))
add("Iron-Deficiency Anemia", cluster(
    ["heavy_periods", "long_periods", "large_clots"],
    "For {s}, iron replaces what you lost and a bleeding treatment stops the ongoing loss. Both are required.",
    "Options for bleeding include tranexamic acid, a hormone IUD, birth-control pills, or treatment of fibroids or polyps. A doctor matches these to your clot history and pregnancy plans.",
    {
        "heavy_periods": "Tell the doctor how often you soak protection. That decides how fast to move beyond iron tablets.",
        "long_periods": "Long periods are logged in days. More than seven days plus anemia should trigger a gynecology plan.",
        "large_clots": "Large clots support the story of heavy loss. Describe their size at the visit.",
    },
    urgency="soon",
))
add("Iron-Deficiency Anemia", cluster(
    ["ice_craving", "pica", "brittle_nails", "spoon_nails", "sore_tongue", "cracks_mouth", "hair_shedding", "restless_legs"],
    "For {s}, the treatment is restoring iron, not a cream or a mouthwash alone. These signs are classic of iron deficiency.",
    "Take iron as prescribed and recheck ferritin. Separate it from thyroid medicine, tea, and coffee. A vitamin C-rich food helps absorption.",
    {
        "ice_craving": "Craving ice often fades as ferritin rises. Keep using it as a symptom to report, including if it returns later.",
        "pica": "Craving dirt, starch, or other non-food items is a medical sign. Stop eating those items because some are harmful, and tell the doctor so iron can be confirmed.",
        "brittle_nails": "Brittle nails need months of normal iron to change. Topical nail products are cosmetic.",
        "spoon_nails": "Nails that curve up like a spoon are advanced iron deficiency. They need a clinician, not a nail salon cure.",
        "sore_tongue": "A sore smooth tongue improves as iron returns. A clinician should see a tongue ulcer that does not heal.",
        "cracks_mouth": "Cracks at the corners of the mouth need iron replacement. A bland ointment protects the skin while it heals. Check that yeast is not also present.",
        "hair_shedding": "Increased shedding slows after iron stores recover, with a lag of months. Check thyroid if shedding continues.",
        "restless_legs": "An urge to move the legs at night can improve when iron stores, including ferritin, are rebuilt. Ask before using a restless-leg medicine.",
    },
))
add("Iron-Deficiency Anemia", cluster(
    ["chest_pain", "black_stools"],
    "For {s}, seek urgent care. Chest pain on effort can mean the heart is strained by anemia. Black tarry stools can mean bleeding in the gut.",
    "Do not start iron and stay home with these two symptoms. Iron tablets themselves can darken stool, but tarry black stool with weakness, or chest pain, still needs an urgent exam.",
    {
        "chest_pain": "Chest pain on effort is an emergency until a clinician says otherwise. Sit, and call emergency services if the pain is severe, spreading, or comes with sweating or breathlessness.",
        "black_stools": "Black tarry stools need urgent assessment for gastrointestinal bleeding. Stop anti-inflammatory tablets such as ibuprofen unless a doctor tells you to continue.",
    },
    urgency="urgent",
))
add("Iron-Deficiency Anemia", cluster(
    ["pregnancy", "vegetarian_low_iron"],
    "For {s}, a prenatal or primary clinician should check iron and prescribe a pregnancy-safe or diet-aware plan.",
    "Food sources such as meat, legumes, and iron-fortified foods help, with a vitamin C-rich food in the same meal. Tea and coffee at the meal reduce absorption. Tablets or intravenous iron are added when diet is not enough.",
    {
        "pregnancy": "Pregnancy raises iron need. Use the prenatal plan you were given rather than extra pills from a shop stacked on top. Severe anemia in pregnancy is a prompt obstetric issue.",
        "vegetarian_low_iron": "A diet with very little iron-rich food can be adjusted with legumes, tofu, fortified grains, and vitamin C. A dietitian helps. Labs decide if tablets are also needed. This is especially important with heavy periods.",
    },
    urgency="soon",
))

# --- Gestational diabetes ---
add("Gestational Diabetes", cluster(
    ["previous_gdm", "routine_screen", "screen_window", "no_symptoms", "prior_large_baby", "baby_measuring_large", "sugar_in_urine", "family_diabetes", "extra_fluid_told", "prior_pregnancy_sugar_problem", "high_result_letter", "need_repeat_test"],
    "For {s}, complete the pregnancy glucose test your obstetric team orders. Most people with gestational diabetes have no symptoms, so the test is the way it is found.",
    "If the result is high, treatment starts with a pregnancy dietitian, glucose checks, and agreed activity. Insulin or another pregnancy-used medicine is added only by that team if targets are missed.",
    {
        "previous_gdm": "Gestational diabetes before means you should be tested as early as your team advises in this pregnancy, not only at the usual later window.",
        "routine_screen": "A routine sugar test that is due should be booked now. Do not skip it because you feel well.",
        "screen_window": "Being in the weeks when the test is usually done is the cue to attend, even without thirst or other symptoms.",
        "no_symptoms": "No symptoms at the screening visit is common. The blood test still matters.",
        "prior_large_baby": "A past large baby is a reason for careful glucose testing and growth scans in this pregnancy.",
        "baby_measuring_large": "Being told this baby is measuring large leads to glucose review and follow-up growth checks, not to a crash diet.",
        "sugar_in_urine": "Sugar in the urine at a prenatal visit is a reason for a formal glucose test. It is not diagnosed or treated from the dipstick alone.",
        "family_diabetes": "A parent or sibling with diabetes raises your chance. Attend the screen and mention the family history.",
        "extra_fluid_told": "Extra fluid around the baby is managed with glucose review and obstetric follow-up.",
        "prior_pregnancy_sugar_problem": "A past high sugar result means follow this pregnancy's test schedule closely and keep the records.",
        "high_result_letter": "A message that a sugar test was high should lead to the next test or the treatment visit within the time the message states. Do not start a family member's diabetes pills.",
        "need_repeat_test": "Being asked back for a longer sugar test is the diagnostic step. Finish it even if you feel normal that morning.",
    },
    urgency="soon",
))
add("Gestational Diabetes", cluster(
    ["extra_thirst", "dry_mouth", "frequent_urination", "night_urination", "fatigue", "blurred_vision", "increased_hunger", "nausea", "headache", "dizziness", "weight_gain_fast", "slow_healing"],
    "For {s} in pregnancy, tell your obstetric clinician and get glucose checked. Do not start non-pregnancy diabetes drugs.",
    "If gestational diabetes is confirmed, follow the meal plan, check glucose at the times you were shown, and walk or do other approved activity. Call the pregnancy team for readings above the numbers they gave you.",
    {
        "extra_thirst": "Extra thirst in pregnancy can be many things, including high sugar. Report it rather than only drinking more.",
        "dry_mouth": "A dry mouth is reported with thirst. Sip water, and still get the glucose advice.",
        "frequent_urination": "Urinating more than expected needs a urine infection check and a glucose check. Do not cut fluids.",
        "night_urination": "Waking often at night is common late in pregnancy and still worth a urine and glucose review if it is new or extreme.",
        "fatigue": "Tiredness is common in pregnancy. Sudden exhaustion with thirst or blurred vision should be reported.",
        "blurred_vision": "Blurred vision that comes and goes needs prompt obstetric advice and a glucose check. Sudden vision loss is emergency care.",
        "increased_hunger": "Increased hunger is managed with the pregnancy meal pattern of regular balanced meals, not with skipped meals or diet pills.",
        "nausea": "Nausea is not treated with diabetes tablets. If you cannot keep food or fluids down, contact pregnancy care, because dehydration and ketones matter.",
        "headache": "Headaches in pregnancy need a blood-pressure check. A severe headache, visual change, or swelling of the face and hands can be preeclampsia and is urgent.",
        "dizziness": "Dizziness should be reported. Fainting, chest pain, or vaginal bleeding makes it urgent obstetric care.",
        "weight_gain_fast": "Weight rising very quickly is reviewed by the pregnancy team. Do not start a restrictive diet. Sudden swelling needs a blood-pressure check.",
        "slow_healing": "Cuts that heal slowly should be seen so infection and high glucose are both addressed. Do not use leftover antibiotics.",
    },
    urgency="soon",
))
add("Gestational Diabetes", cluster(
    ["recurrent_thrush", "urine_infections", "burning_urination"],
    "For {s} in pregnancy, get examined. Yeast is treated with a pregnancy-safe topical azole. A urine infection needs a pregnancy-safe antibiotic after a culture. Both are reasons to look at glucose.",
    "Do not use oral fluconazole in pregnancy unless a specialist specifically directs it. Do not use leftover antibiotics.",
    {
        "recurrent_thrush": "Yeast that keeps returning in pregnancy needs a clinician, a pregnancy-safe topical treatment, and a glucose review.",
        "urine_infections": "Urine infections that keep returning need cultures and pregnancy-safe antibiotics. Kidney infection in pregnancy is urgent.",
        "burning_urination": "Burning when urinating in pregnancy needs a urine test promptly. Fever, back pain, or vomiting means same-day obstetric care.",
    },
    urgency="soon",
))


GDM_OVERRIDE = {
    "hot_flashes": (
        "soon",
        "Feeling suddenly hot in pregnancy is not treated with menopause hormone therapy.",
        "Tell your obstetric team, drink water, and dress in layers. Do not start hormones or diabetes pills from home.",
        "A measured fever, a severe headache, vision change, or feeling very unwell needs same-day pregnancy care.",
    ),
    "severe_period_pain": (
        "urgent",
        "Severe belly or period-type pain in pregnancy is not gestational diabetes. Call your obstetric team the same day.",
        "Do not take ibuprofen or other anti-inflammatory pain tablets in pregnancy unless that team tells you to.",
        "Heavy bleeding, one-sided pain, fainting, shoulder-tip pain, or fever is emergency obstetric care.",
    ),
    "bleeding_after_sex": (
        "soon",
        "Bleeding after sex in pregnancy needs a call to your obstetric team. Do not wait for a routine Pap.",
        "Note the amount and any pain, cramping, or fluid, and avoid sex until you have been advised.",
        "Heavy bleeding, strong pain, leaking fluid, or less baby movement is emergency obstetric care.",
    ),
    "one_sided_pelvic_pain": (
        "urgent",
        "Sudden pain on one side in pregnancy needs same-day obstetric care to rule out ectopic pregnancy and other emergencies.",
        "Do not eat or drink if you may need urgent surgery, and do not take anti-inflammatory pain tablets unless the pregnancy team has said they are safe.",
        "Call emergency services if you faint, vomit, bleed heavily, or have shoulder-tip pain.",
    ),
}


def guide_for(condition, symptom_id, symptom):
    if condition == "Gestational Diabetes" and symptom_id in GDM_OVERRIDE:
        urgency, a, b, c = GDM_OVERRIDE[symptom_id]
        return urgency, fmt(a, symptom), fmt(b, symptom), fmt(c, symptom)
    specific = SPECIFIC.get(condition, {}).get(symptom_id)
    if specific:
        urgency, a, b, c = specific
        return urgency, fmt(a, symptom), fmt(b, symptom), fmt(c, symptom)
    return decoy(symptom_id, symptom, condition)


def main():
    with SRC.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    missing_disease = sorted({r["condition"] for r in rows} - set(DISEASE))
    if missing_disease:
        raise SystemExit(f"missing disease text: {missing_disease}")

    out_rows = []
    fallback = []
    for r in rows:
        urgency, w1, w2, w3 = guide_for(r["condition"], r["symptom_id"], r["symptom"])
        if r["symptom_id"] not in SPECIFIC.get(r["condition"], {}):
            fallback.append((r["condition"], r["symptom_id"], r["weight"]))
        out_rows.append({
            "folder": r["folder"],
            "condition": r["condition"],
            "symptom_id": r["symptom_id"],
            "symptom": r["symptom"],
            "weight": r["weight"],
            "urgency": urgency,
            "treatment_1": w1,
            "treatment_2": w2,
            "treatment_3": w3,
        })

    from extra_female_guides import extra_rows
    out_rows.extend(extra_rows())

    fields = list(out_rows[0].keys())
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"rows={len(out_rows)} fallback={len(fallback)} out={OUT}")
    for item in fallback:
        print("FALLBACK", "|".join(item))


if __name__ == "__main__":
    main()

