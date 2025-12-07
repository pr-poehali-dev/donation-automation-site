import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import Icon from '@/components/ui/icon';
import { useToast } from '@/hooks/use-toast';

const Index = () => {
  const [nickname, setNickname] = useState('');
  const [amount, setAmount] = useState('');
  const [showPayment, setShowPayment] = useState(false);
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!nickname || !amount) {
      toast({
        title: "Ошибка",
        description: "Пожалуйста, заполните все поля",
        variant: "destructive"
      });
      return;
    }

    setShowPayment(true);
  };

  const handlePaymentConfirm = () => {
    toast({
      title: "Заявка отправлена!",
      description: "Администратор получил уведомление о вашей оплате",
    });
  };

  if (showPayment) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 animate-fade-in">
        <Card className="w-full max-w-2xl shadow-2xl border-2 border-primary/20 animate-scale-in">
          <CardHeader className="text-center space-y-4 pb-8">
            <div className="mx-auto w-20 h-20 bg-primary rounded-full flex items-center justify-center animate-scale-in">
              <Icon name="CreditCard" className="text-white" size={40} />
            </div>
            <CardTitle className="text-4xl font-bold text-primary">Реквизиты для оплаты</CardTitle>
            <CardDescription className="text-lg">
              Переведите <span className="font-bold text-primary text-xl">{amount} донат рублей</span> на указанные реквизиты
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-8 rounded-xl border-2 border-primary/30 space-y-6">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Icon name="Wallet" className="text-primary" size={24} />
                  <Label className="text-lg font-semibold text-primary">Номер карты</Label>
                </div>
                <div className="bg-white p-4 rounded-lg border border-primary/20">
                  <p className="text-2xl font-mono font-bold text-foreground tracking-wider">
                    2202 2026 5566 7788
                  </p>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Icon name="User" className="text-primary" size={24} />
                  <Label className="text-lg font-semibold text-primary">Получатель</Label>
                </div>
                <div className="bg-white p-4 rounded-lg border border-primary/20">
                  <p className="text-xl font-semibold text-foreground">ИВАН ИВАНОВИЧ И.</p>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Icon name="Hash" className="text-primary" size={24} />
                  <Label className="text-lg font-semibold text-primary">Комментарий к переводу</Label>
                </div>
                <div className="bg-white p-4 rounded-lg border border-primary/20">
                  <p className="text-xl font-semibold text-foreground">Донат для {nickname}</p>
                </div>
              </div>
            </div>

            <div className="bg-yellow-50 border-2 border-yellow-400 rounded-lg p-4 flex gap-3">
              <Icon name="AlertCircle" className="text-yellow-600 flex-shrink-0" size={24} />
              <p className="text-sm text-yellow-800">
                <strong>Важно!</strong> Обязательно укажите комментарий при переводе, чтобы мы могли зачислить донат рубли на ваш аккаунт
              </p>
            </div>

            <div className="flex gap-4">
              <Button 
                onClick={handlePaymentConfirm}
                className="flex-1 h-14 text-lg font-semibold transition-all hover:scale-105"
                size="lg"
              >
                <Icon name="Check" className="mr-2" size={24} />
                Оплатил
              </Button>
              <Button 
                onClick={() => setShowPayment(false)}
                variant="outline"
                className="h-14 px-6 border-2 transition-all hover:scale-105"
                size="lg"
              >
                <Icon name="ArrowLeft" className="mr-2" size={20} />
                Назад
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 animate-fade-in">
      <Card className="w-full max-w-md shadow-2xl border-2 border-primary/20 animate-scale-in">
        <CardHeader className="text-center space-y-4 pb-8">
          <div className="mx-auto w-20 h-20 bg-primary rounded-full flex items-center justify-center animate-scale-in">
            <Icon name="Coins" className="text-white" size={40} />
          </div>
          <CardTitle className="text-4xl font-bold text-primary">Донат рубли</CardTitle>
          <CardDescription className="text-base">
            Пополните свой баланс донат рублей на сервере
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-3">
              <Label htmlFor="nickname" className="text-base font-semibold flex items-center gap-2">
                <Icon name="User" className="text-primary" size={20} />
                Ваш игровой ник
              </Label>
              <Input
                id="nickname"
                placeholder="Введите ник на сервере"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                className="h-12 text-base border-2 focus:border-primary transition-all"
              />
            </div>

            <div className="space-y-3">
              <Label htmlFor="amount" className="text-base font-semibold flex items-center gap-2">
                <Icon name="DollarSign" className="text-primary" size={20} />
                Количество донат рублей
              </Label>
              <Input
                id="amount"
                type="number"
                placeholder="Введите сумму"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="h-12 text-base border-2 focus:border-primary transition-all"
                min="1"
              />
            </div>

            <Button 
              type="submit" 
              className="w-full h-14 text-lg font-semibold transition-all hover:scale-105"
              size="lg"
            >
              <Icon name="ArrowRight" className="mr-2" size={24} />
              Продолжить к оплате
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default Index;
