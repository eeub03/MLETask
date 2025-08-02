import pandera.pandas as pa
import pandas as pd


class InputSchema(pa.DataFrameModel):
    claim_status: pa.typing.Series[int]
    age: pa.typing.Series[int] = pa.Field(ge=18)
    height_cm: pa.typing.Series[int] = pa.Field(ge=30, le=400)
    weight_kg: pa.typing.Series[int] = pa.Field(ge=1, le=1000)
    income: pa.typing.Series[int] = pa.Field(ge=0)
    financial_hist_1: pa.typing.Series[float]
    financial_hist_2: pa.typing.Series[float]
    financial_hist_3: pa.typing.Series[float]
    financial_hist_4: pa.typing.Series[float]
    credit_score_1: pa.typing.Series[int] = pa.Field(ge=0, le=999)
    credit_score_2: pa.typing.Series[int] = pa.Field(ge=0, le=700)
    credit_score_3: pa.typing.Series[int] = pa.Field(ge=0, le=710)
    insurance_hist_1: pa.typing.Series[float]
    insurance_hist_2: pa.typing.Series[float]
    insurance_hist_3: pa.typing.Series[float]
    insurance_hist_4: pa.typing.Series[float]
    insurance_hist_5: pa.typing.Series[float]
    bmi: pa.typing.Series[int] = pa.Field(ge=10, le=100)
    gender: pa.typing.Series[pd.CategoricalDtype]
    marital_status: pa.typing.Series[pd.CategoricalDtype]
    occupation: pa.typing.Series[pd.CategoricalDtype]
    location: pa.typing.Series[pd.CategoricalDtype]
    prev_claim_rejected: pa.typing.Series[pd.CategoricalDtype]
    known_health_conditions: pa.typing.Series[pd.CategoricalDtype]
    uk_residence: pa.typing.Series[pd.CategoricalDtype]
    family_history_1: pa.typing.Series[pd.CategoricalDtype]
    family_history_2: pa.typing.Series[pd.CategoricalDtype]
    family_history_4: pa.typing.Series[pd.CategoricalDtype]
    family_history_5: pa.typing.Series[pd.CategoricalDtype]
    product_var_1: pa.typing.Series[pd.CategoricalDtype]
    product_var_2: pa.typing.Series[pd.CategoricalDtype]
    product_var_3: pa.typing.Series[pd.CategoricalDtype]
    health_status: pa.typing.Series[pd.CategoricalDtype]
    driving_record: pa.typing.Series[pd.CategoricalDtype]
    previous_claim_rate: pa.typing.Series[pd.CategoricalDtype]
    education_level: pa.typing.Series[pd.CategoricalDtype]
    n_dependents: pa.typing.Series[pd.CategoricalDtype]
