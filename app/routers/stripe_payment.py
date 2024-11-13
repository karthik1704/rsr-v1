import json
from typing import Annotated, List

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.dependencies.auth import get_current_user
from app.models.stripe_payment import StripePayment
from app.models.users import User
from app.schemas.stripe_payment import PaymentCreate, PaymentUpdate

from ..database import get_async_db

router = APIRouter(prefix="/stripe-payments", tags=["stripe-payments"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
current_user_dep = Annotated[dict, Depends(get_current_user)]

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@router.post("/")
async def create_payment_intent(payment: PaymentCreate, db: db_dep, current_user: current_user_dep):

    user = await User.get_one(db, [User.id == current_user['id']])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    print("web hook", endpoint_secret)

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount),
            currency="gbp",
            receipt_email=user.email,
            
            # payment_method_types=[
            #    "card",
            # ],
            # payment_method_types=["card", ],  # Any methods you want to support
            # confirmation_method="manual",
            metadata={
                "user_id": current_user['id'],
                "email": current_user['email'], 
            }
        )

        # print(json.dumps(intent, indent=2))

        db_payment = StripePayment(
            amount=payment.amount,
            currency="gbp",
            status="pending",
            stripe_payment_intent_id=intent.id,
            user_id=current_user['id'],
            # payment_id=intent.id
        )
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)

        return {"clientSecret": intent.client_secret, "paymentId": db_payment.stripe_payment_intent_id}
        # return {
        #     "clientSecret": intent.client_secret,
        # }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update-payment-status")
async def update_payment_status(
    payment_update: PaymentUpdate, db: db_dep, current_user: current_user_dep
):
    db_payment = await StripePayment.get(
        db, [StripePayment.payment_id == payment_update.payment_id]
    )
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    db_payment.status = payment_update.status
    if payment_update.failure_code:
        db_payment.failure_code = payment_update.failure_code
    if payment_update.failure_message:
        db_payment.failure_message = payment_update.failure_message
    await db.commit()
    await db.refresh(db_payment)

    return {"message": "Payment status updated successfully"}


@router.post("/webhook/", status_code=status.HTTP_200_OK)
async def stripe_webhook(request: Request, db: db_dep):
    payload = await request.body()
    # print(request.headers)
    print("Received payload:")
    print(json.dumps(json.loads(payload), indent=2))
    sig_header = request.headers.get("stripe-signature")
    # print(sig_header)
    print('endpoint_secret', endpoint_secret)
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        print("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid signature {str(endpoint_secret)}")

    # Database update logic (Example: AsyncSession injection)
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        payment_id = payment_intent["id"]
        print(payment_id)
        # Update the payment status in the database
        print("succeeded")
        # Update the payment status in the database
        await StripePayment.update(db, payment_id, status="succeeded")

        print('user_id', payment_intent["metadata"]["user_id"])
        user_id = int(payment_intent["metadata"]["user_id"])
        # Update user's expiry date
        user = await User.get_one(db, [User.id == user_id])
        if user:
            from datetime import datetime, timedelta
            new_expiry_date = datetime.now() + timedelta(days=90)  # 3 months
            await User.update(db, user.id, expiry_date=new_expiry_date)
        
        await db.commit()

    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        payment_id = payment_intent["id"]
        failure_reason = payment_intent["last_payment_error"]["message"]
        # Update the failure status in the database
        print("failed")
        await StripePayment.update(
            db, payment_id, status="failed", failure_reason=failure_reason
        )
        await db.commit()

    return {"status": "success"}
